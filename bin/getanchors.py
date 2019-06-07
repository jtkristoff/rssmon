#!/usr/bin/env python3

import requests
import sys

url  = 'https://atlas.ripe.net/api/v2/anchors/'
anchors = 0
max_anchors = 1000

# max_anchors might exceed threshold, but we won't fetch pages indefinitely
while url != None and anchors <= max_anchors:
    try:
        resp = requests.get(url=url, timeout=5)
    except:
        print('Oops')
        raise
 
    data = resp.json()

    for anchor in data['results']:
        sys.stdout.write("id: %d|country: %s|ip_v4: %s"
            % (anchor['id'], anchor['country'], anchor['ip_v4']))
        if anchor['ip_v6'] == None:
            sys.stdout.write("\n")
        else:
            sys.stdout.write("|ip_v6: %s\n" % (anchor['ip_v6']))
        anchors += 1

    url = data['next']

sys.stdout.write("number of anchors: %d\n" % (anchors))
