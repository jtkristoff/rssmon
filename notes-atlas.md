# RIPE Atlas notes

## Built-in Measurements

Relevant definitions extracted from the RIPE Atlas [Built-in
Measurements](https://atlas.ripe.net/docs/built-in/) page.

| **Measurement range** | **Measurement ID** | **Meaning / Target**         | **Frequency** |
|:--------------------- |:------------------ |:---------------------------- |:------------- |
| **10000 - 10999**     |                    | **IPv4 DNS SOA and anycast** |               |
|                       |                    |                              |               |
|                       | 100xx              | IPv4 UDP DNS SOA             | 1800 seconds  |
|                       | 101xx              | IPv4 TCP DNS SOA             | 1800 seconds  |
|                       |                    |                              |               |
|                       | 110xx              | IPv6 UDP DNS SOA             | 1800 seconds  | 
|                       | 111xx              | IPv6 TCP DNS SOA             | 1800 seconds  |

Relevant measurement offsets from the RIPE Atlas [Built-in
Measurements](https://atlas.ripe.net/docs/built-in/) page.

| **Destination name** | **Measurement Offset** | **Ping (frequency: 240)** | **Traceroute (frequency: 1800)** | **DNS**     |
|:-------------------- |:---------------------- |:------------------------- |:-------------------------------- |:----------- |
| A.root-servers.net   | 9                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| B.root-servers.net   | 10                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| C.root-servers.net   | 11                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| D.root-servers.net   | 12                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| E.root-servers.net   | 13                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| F.root-servers.net   | 4                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| G.root-servers.net   | 14                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| H.root-servers.net   | 15                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| I.root-servers.net   | 5                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| J.root-servers.net   | 16                     | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| K.root-servers.net   | 1                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| L.root-servers.net   | 8                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |
| M.root-servers.net   | 6                      | IPv4 + IPv6               | IPv4 + IPv6                      | IPv4 + IPv6 |

## Example RESTful URLs

* foobar

   `https://atlas.ripe.net/api/v2/measurements/10008`

* bar

   `https://atlas.ripe.net/api/v2/measurements/10009`

* baz

    `https://atlas.ripe.net/api/v2/measurements/10009/latest/?probe_ids=6489`

* qux 

    `https://atlas.ripe.net/api/v2/measurements/10009/results/?probe_ids=6489&start=1560180000`
