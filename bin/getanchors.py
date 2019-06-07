#!/usr/bin/env python3

import requests
import psycopg2
import sys

from psycopg2.extensions import AsIs

url  = 'https://atlas.ripe.net/api/v2/anchors/'
anchors = 0
max_anchors = 1000

conn = psycopg2.connect("dbname=rssmon")
cur  = conn.cursor()

# max_anchors might exceed threshold, but we won't fetch pages indefinitely
while url != None and anchors <= max_anchors:
    try:
        resp = requests.get(url=url, timeout=5)
    except:
        print('Oops')
        raise
 
    data = resp.json()

    for anchor in data['results']:
        if anchor['is_disabled'] == True:
            continue

        columns = []
        columns.extend(['id','probe','country','city','ip_v4','as_v4'])
        if anchor['ip_v6'] == None:
            pass
        else:
            columns.extend(['ip_v6','as_v6'])

        insert_statement = 'INSERT INTO anchor (%s) values %s'
        values  = [anchor[column] for column in columns]

        # saw a v6addr with leading space, so we hack
        for index, value in enumerate(values):
            if isinstance(value, str):
                values[index] = value.strip()

        cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))

        anchors += 1

    url = data['next']

conn.commit()
cur.close()
conn.close()

# TODO: send this to syslog
sys.stdout.write("number of anchors: %d\n" % (anchors))
