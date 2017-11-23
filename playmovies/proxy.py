#!/bin/bash
# To generate proxy ip for browsing from the US 
# Uses gimmeproxy api
import time
import random
import requests
from bs4 import BeautifulSoup

# list from https://www.us-proxy.org/
# final thing expected to crawl from the site

URL = 'https://www.us-proxy.org'

def generateProxy():
    # randomize the proxy ips
    while True:
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                break
        except Exception as e:
            print(e)
            print("Waiting...")
            time.sleep(300)
    # Get the soup
    soup = BeautifulSoup(response.content, 'html.parser')
    ips = []
    for row in soup.find_all('tr'):
        ip = []
        for column in row:
            ip.append(column.get_text())
        ips.append(ip)
    
    usables = ips[1:-1]
    # print([i for i in ips if 'elite proxy' in i])
    proxy_list = [i[0]+':'+i[1] for i in usables if 'elite proxy' in i]
    print(len(proxy_list))
    random_ipport = random.choice(proxy_list)            
    # ip, port = random_ipport.split(':')
    # return ip, port
    return random_ipport



# Luminati proxy
import urllib2
import json

def newIP():
    username = 'lum-customer-hl_c5fdc81d-zone-zone1'
    password = 'l7drwpqxam3y'
    port = 22225

    proxy_url = 'http://lum-customer-hl_c5fdc81d-zone-zone1:l7drwpqxam3y@zproxy.luminati.io:22225'
    print(proxy_url)
    proxy_handler = urllib2.ProxyHandler({
        'http': 'http://lum-customer-hl_c5fdc81d-zone-zone1:l7drwpqxam3y@zproxy.luminati.io:22225'
    })
    opener = urllib2.build_opener(proxy_handler)
    a = urllib2.install_opener(opener)
    print(a)

    cont =  urllib2.urlopen('http://lumtest.com/myip.json').read()
    data = json.loads(cont)
    print(data)
    return "%s:%s" % (data["ip"], data["asn"]["asnum"])
