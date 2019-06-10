#!/usr/bin/env python3

import requests
import psycopg2
import sys

from psycopg2.extensions import AsIs
from datetime import datetime, timedelta, timezone

# starting epoch 31 days ago
start_time = int((datetime.now(tz=timezone.utc) - timedelta(days=31)).timestamp())
stop_time = start_time + 86400
now = int(datetime.now(tz=timezone.utc).timestamp())

# built in DNS SOA measurements <https://atlas.ripe.net/docs/built-in/>
measure_url = 'https://atlas.ripe.net/api/v2/measurements'
# measure_id/results/?probe_ids=[probe_ids]&start=[unix_time]
# e.g. 10009/results/?probe_ids=6489&start=1560180000
# 31 days ago from today 2019-06-10: 1557519181

### TODO: not all probes support IPv6, need to skip those
soa_prefix = {
    'v4_udp' : '100',
    'v4_tcp' : '101',
    'v6_udp' : '110',
    'v6_tcp' : '111'
}
server_offsets = {
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

### TODO: need start and stop time to fetch more than a few days measurements
###       otherwise the request takes too long (or response is too large)
###       pick a start time and get data for intervals beginning from there

conn = psycopg2.connect("dbname=rssmon")
cur  = conn.cursor()
cur.execute("SELECT probe,ip_v6 FROM anchor")
probes = cur.fetchall()

for probe in probes:
    sys.stdout.write("probe: %d\n" % (probe[0]))

    for type,value in soa_prefix.items():
        if (type == 'v6_udp' or type == 'v6_tcp') and probe[1] is None:
            continue

        for root,id in server_offsets.items():

            url = "%s/%s/results?probe_ids=%d&start=%d&stop=%d" % (measure_url, value + id, probe[0], start_time, stop_time)
            print(url)
            sys.exit
            try:
                resp = requests.get(url=url, timeout=5)
            except:
                print('Oops')
                raise

            data = resp.json()
            ### TMP
            print(data)

cur.close()
conn.close()
