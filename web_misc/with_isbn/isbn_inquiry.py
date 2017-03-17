# -*- coding: utf-8 -*-
from difflib import SequenceMatcher
import json
import os
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


class isbn_inquiry():
    def __init__(self, title):
        self.__h = {'User-Agent': UserAgent().random}
        self.__base_url = 'http://bookmeter.com/'
        self.__series_url = self.__base_url + self.__get_id(title)

    def __get_id(self, title):
        r = requests.get(self.__base_url + 's?q=' + title, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            d = soup.find('div', class_='series_list')
            if d is None:
                return ""
            for a in d.find_all('a'):
                if SequenceMatcher(None, title, a.text).ratio() < 0.5:
                    continue
                return a['href']
        return ""

    def __title(self, soup):
        return soup.find('h1', id="title").text[:-4]

    def __latest(self, soup):
        v = soup.find('div', class_='rank_box clearfix')
        return int(v.div.div.span.text)

    def __isbns(self, soup, n=0):
        isbns = []
        for v in soup.find_all('div', class_='rank_box clearfix'):
            d = v.find('div', class_='rank_detail_title')
            if int(v.div.div.span.text) < n:
                break
            print v.div.div.span.text, d.a['href'][3:]
            isbns.append(d.a['href'][3:])
        return isbns[::-1]

    def __has_next(self, soup):
        n = soup.find('div', id='page_navigation')
        return True if n is not None else False

    def __get_next(self, soup, zzz=3, n=0):
        isbns = []
        nex = soup.find('div', id='page_navigation')
        for s in nex.find_all('span', class_=None):
            time.sleep(zzz)
            r = requests.get(self.__series_url + s.a['href'][-4:],
                             headers=self.__h)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'lxml')
                isbns = self.__isbns(soup, n=n) + isbns
        return isbns

    def get_isbn(self, n=0):
        if self.__base_url == self.__series_url:
            return None
        r = requests.get(self.__series_url, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            print self.__title(soup), self.__latest(soup)
            isbns = self.__isbns(soup, n=n)
            if len(isbns) == 20 and self.__has_next(soup):
                isbns = self.__get_next(soup, n=n) + isbns
            return isbns
        return None


def read_isbn(isbn_json):
    isbn_dict = {}
    if os.path.exists(isbn_json):
        with open(isbn_json, 'r') as f:
            isbn_dict = json.load(f)
    return isbn_dict


def update(isbn_dict, titles, zzz=5):
    for t in titles:
        n = 1
        if t in isbn_dict:
            n += len(isbn_dict[t])
        v = isbn_inquiry(t).get_isbn(n)
        if v is not None:
            if t in isbn_dict:
                isbn_dict[t] = isbn_dict[t] + v
            else:
                isbn_dict[t] = v
        else:
            print "Error: could not be resolved with ` ", t, "'..."
        time.sleep(zzz)
    return isbn_dict

if __name__ == '__main__':
    isbn_file = 'isbn2.json'
    isbn_dict = read_isbn(isbn_file)

    titles = [u'鬼滅の刃', u'ワンピース', u'ブラッククローバー',
              u'ちはやふる', u'君に届け', u'あさひなぐ']
    update(isbn_dict, titles)

    with open(isbn_file, 'w') as f:
        f.write(json.dumps(isbn_dict, ensure_ascii=False).encode('utf-8'))
