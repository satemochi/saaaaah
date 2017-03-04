# -*- coding: utf-8 -*-
from difflib import SequenceMatcher
import re
import requests
from bs4 import BeautifulSoup


def check(target):
    title, pub_date = "", ""
    r = requests.get('http://www.kadokawaharuki.co.jp/book/next/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        for dt in soup.find('div', id='left').find_all('dt'):
            if SequenceMatcher(None, target, dt.text).ratio() < 0.5:
                continue
            title = dt.text
            pattern = re.compile('\d{4}/\d{2}/\d{2}')
            for td in dt.findNext('dd').find_all('td'):
                if pattern.match(td.text):
                    pub_date = td.text
                    break
            break
    return (title, pub_date)

if __name__ == '__main__':
    title, pub_date = check(u'あきない世傳　金と銀')
    if title != "":
        print title, pub_date
