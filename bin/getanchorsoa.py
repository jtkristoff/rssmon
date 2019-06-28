#!/usr/bin/env python3

import logging
import psycopg2
import requests
import sys

from datetime import datetime, timedelta, timezone
from logging.handlers import SysLogHandler
from psycopg2.extensions import AsIs
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

syslog = SysLogHandler('/dev/log', facility=SysLogHandler.LOG_LOCAL0)
syslog.setFormatter(logging.Formatter('getanchorsoa: %(message)s'))
logger = logging.getLogger()
logger.addHandler(syslog)

# starting epoch 31 days ago
start_time = int((datetime.now(tz=timezone.utc) - timedelta(days=31)).timestamp())
stop_time = start_time + 86400
now = int(datetime.now(tz=timezone.utc).timestamp())

# built in DNS SOA measurements <https://atlas.ripe.net/docs/built-in/>
measure_url = 'https://atlas.ripe.net/api/v2/measurements'

# measurement id string = prefix + offset
soa_prefix = {
    'v4_udp' : '100',
    'v4_tcp' : '101',
    'v6_udp' : '110',
    'v6_tcp' : '111'
}
server_offset = {
    'A-ROOT' : '09',
    'B-ROOT' : '10',
    'C-ROOT' : '11',
    'D-ROOT' : '12',
    'E-ROOT' : '13',
    'F-ROOT' : '04',
    'G-ROOT' : '14',
    'H-ROOT' : '15',
    'I-ROOT' : '05',
    'J-ROOT' : '16',
    'K-ROOT' : '01',
    'L-ROOT' : '08',
    'M-ROOT' : '06'
}

### XXX: need start and stop time to fetch limited amount of data at a time
###      otherwise the request takes too long (or response is too large)

conn = psycopg2.connect("dbname=rssmon")
cur  = conn.cursor()
cur.execute("SELECT probe,ip_v6 FROM anchor")
probes = cur.fetchall()

### from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

while start_time < now:
    for probe in probes:

        for type,value in soa_prefix.items():
            # skip v6 measurements for non-v6 probes
            if (type == 'v6_udp' or type == 'v6_tcp') and probe[1] is None:
                continue

            for root,id in server_offset.items():

                url = "%s/%s/results?probe_ids=%d&start=%d&stop=%d" % (measure_url, value + id, probe[0], start_time, stop_time)
                # TODO: log to syslog
                sys.stderr.write("### Fetching measurement data: %s\n" % (url))

                try:
                    resp = requests_retry_session().get(url)
                    logger.info('url fetched: %s', url)
                except:
                    ### XXX: is this sufficient?
                    logger.warning('url fetch error: %s', url)
                    continue

                try:
                    data = resp.json()
                except:
                    logger.warning('url decode error: %s', url)
                    continue

                for results in data:
                    try:
                        rt = results['result']['rt']
                    except:
                        rt = -10   # error in measurement

                    ts = datetime.utcfromtimestamp(results['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

                    columns = ['ts','probe','type','ns','rt']
                    values = [ts,probe[0],type,root,rt]
                    insert_statement = 'INSERT INTO measure_soa (%s) VALUES %s'

                    cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
                    conn.commit()

    start_time = stop_time + 1
    stop_time += 86400

conn.commit()
cur.close()
conn.close()
