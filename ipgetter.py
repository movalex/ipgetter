#!/usr/bin/env python
"""
This module is designed to fetch your external IP address from the internet.
It is used mostly when behind a NAT.
It picks your IP randomly from a serverlist to minimize request
overhead on a single server

If you want to add or remove your server from the list contact me on github


API Usage
=========

    >>> import ipgetter
    >>> myip = ipgetter.myip()
    >>> myip
    '8.8.8.8'

    >>> ipgetter.IPgetter().test()

    Number of servers: 47
    IP's :
    8.8.8.8 = 47 ocurrencies


Copyright 2014 phoemur@gmail.com
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See https://www.wtfpl.net/ for more details.
"""

import re
import random
import ssl

from sys import version_info

PY3K = version_info >= (3, 0)

if PY3K:
    import urllib.request as urllib
else:
    import urllib2 as urllib

__version__ = "0.6"


def myip():
    return IPgetter().get_externalip()


class IPgetter(object):

    """
    This class is designed to fetch your external IP address from the internet.
    It is used mostly when behind a NAT.
    It picks your IP randomly from a serverlist to minimize request overhead
    on a single server
    """

    def __init__(self):
        self.server_list = [
            "http://checkip.dyndns.org/plain",
            "http://lawrencegoetz.com/programs/ipinfo/",
            "http://myipnumber.com/my-ip-address.asp",
            "https://api.ipify.org",
            "https://bobborst.com/tools/whatsmyip/",
            "https://canyouseeme.org/",
            "https://check.torproject.org/",
            "https://diagnostic.opendns.com/myip",
            "https://displaymyip.com/",
            "https://geoiptool.com/",
            "https://getmyipaddress.org/",
            "https://httpbin.org/ip",
            "https://icanhazip.com/",
            "https://ifconfig.me/ip",
            "https://ip-adress.com/",
            "https://ip-adress.eu/",
            "https://ipchicken.com/",
            "https://ipecho.net/plain",
            "https://mon-ip.com/en/my-ip/",
            "https://my-ip-address.net/",
            "https://myexternalip.com/raw",
            "https://privateinternetaccess.com/pages/whats-my-ip/",
            "https://tracemyip.org/",
            "https://trackip.net/",
            "https://whatsmydns.net/whats-my-ip-address.html",
            "https://whatsmyip.net/",
            "https://wtfismyip.com/text",
        ]

    def get_externalip(self):
        """
        This function gets your IP from a random server
        """

        myip = ""
        for i in range(5):
            myip = self.fetch(random.choice(self.server_list))
            if myip != "":
                return myip
            else:
                continue
        return ""

    def fetch(self, server):
        """
        This function gets your IP from a specific server.
        """
        url = None

        opener = urllib.build_opener()
        addheaders = {
            "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
        }

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            req = urllib.Request(server, None, addheaders)
            url = urllib.urlopen(req, timeout=2, context=ctx)
            content = url.read()

            if PY3K:
                try:
                    content = content.decode("UTF-8")
                except UnicodeDecodeError:
                    content = content.decode("ISO-8859-1")

            m = re.search(
                "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                content,
            )
            myip = m.group(0)
            return myip if len(myip) > 0 else ""
        except Exception as e:
            print("Exception raised on url {} -- ".format(server), e)
            return ""
        finally:
            if url:
                url.close()

    def test(self):
        """
        This functions tests the consistency of the servers
        on the list when retrieving your IP.
        All results should be the same.
        """

        resultdict = {}
        for server in self.server_list:
            resultdict.update(**{server: self.fetch(server)})

        ips = sorted(resultdict.values())
        ips_set = set(ips)
        print("\nNumber of servers: {}".format(len(self.server_list)))

        for ip, occurence in zip(ips_set, map(lambda x: ips.count(x), ips_set)):
            print(
                "{0} = {1} ocurrenc{2}".format(
                    ip if len(ip) > 0 else "broken server",
                    occurence,
                    "e" if occurence == 1 else "ies",
                )
            )
        print("\n")
        if any([i == "" for i in resultdict.values()]):
            print("\n________list of failed servers_______")
            for _url, _ip in resultdict.items():
                if _ip == "":
                    print(_url)
        print("\n")
        return resultdict


if __name__ == "__main__":
    print(myip())
