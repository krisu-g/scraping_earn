"""https://pypi.org/project/Proxy-List-Scrapper/
"""
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import pandas as pd
import os
from datetime import datetime, timedelta
import requests
from itertools import cycle
import traceback
import random
import time

SSL = 'https://www.sslproxies.org/',
GOOGLE = 'https://www.google-proxy.net/',
ANANY = 'https://free-proxy-list.net/anonymous-proxy.html',
UK = 'https://free-proxy-list.net/uk-proxy.html',
US = 'https://www.us-proxy.org/',
NEW = 'https://free-proxy-list.net/',
SPYS_ME = 'http://spys.me/proxy.txt',
PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all',
PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
ALL = 'ALL'


def get_random_headder():
    with open('user-agents.txt', 'r') as f:
        user_agent_list = f.read().splitlines()

    headers = {
        "User-Agent": random.choice(user_agent_list),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    return headers


def get_proxies(filename='proxies.txt', proxy_category='SSL', force_get_proxies=False, max_minutes_actual=15):
    is_proxies_up_to_date = False
    if os.path.isfile(filename) and not force_get_proxies:
        file_mod_time = datetime.fromtimestamp(os.stat(filename).st_mtime)  # This is a datetime.datetime object!
        now = datetime.today()
        max_delay = timedelta(minutes=max_minutes_actual)
        if now - file_mod_time < max_delay:
            is_proxies_up_to_date = True

    if not is_proxies_up_to_date:
        print('Scraping proxies...')
        scrapper = Scrapper(category=proxy_category, print_err_trace=False)
        data = scrapper.getProxies()
        df = pd.DataFrame([f'{proxy_elem.ip}:{proxy_elem.port}' for proxy_elem in data.proxies], columns=['IP:Port'])
        df.to_csv('proxies.txt', index=False)
    else:
        print(f'Proxies up-to-date. Taking from {filename} file...')
        with open(filename, 'r') as f:
            df = pd.DataFrame(f.readlines(), columns=['IP:Port'])
            df['IP:Port'] = df['IP:Port'].str.strip()

    return set(df['IP:Port'])


if __name__ == '__main__':
    proxies = get_proxies(filename='proxies.txt', proxy_category='SSL', force_get_proxies=False, max_minutes_actual=15)

    print("Total Proxies found:", len(proxies))

    proxy_pool = cycle(proxies)
    url = 'https://httpbin.org/ip'
    for i in range(1, 11):
        proxy = next(proxy_pool)
        print(f"Request #{i}, proxy: {proxy}")
        try:
            wait_time = random.uniform(5, 9)
            time.sleep(random.uniform(5, 9))
            response = requests.get(url,
                                    proxies={
                                        "http": 'http://' + proxy,
                                        "https": 'https://' + proxy
                                    },
                                    headers=get_random_headder())
            print(response.json(), 'Wait time:', wait_time)
        except Exception as e:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error: ", e)