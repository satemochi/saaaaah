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
        self.__base_url = 'https://bookmeter.com/'
        self.__series_url = self.__base_url + self.__get_id(title)

    def __get_id(self, title):
        r = requests.get(self.__base_url + 'search?keyword=' + title,
                         headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            u = soup.find('ul', class_='series__list')
            if u is None:
                return ""
            for a in u.find_all('a'):
                if SequenceMatcher(None, title, a.text).ratio() < 0.75:
                    continue
                return a['href']
        return ""

    def __title(self, soup):
        return soup.find('h1', class_="header__title").div.text.split(' ')[0]

    def __latest(self, soup):
        return soup.find('div', class_="content__count").text[:-1]

    def __has_next(self, soup):
        n = soup.find('ul', class_='bm-pagination')
        return True if n is not None else False

    def __get_next(self, soup, stop_isbn, c=1, zzz=3):
        isbns = []
        nex = soup.find('ul', class_='bm-pagination')
        for s in nex.find_all('li', class_=None):
            if s.a.text in u'最初前次最後' or int(s.a.text) != c + 1:
                continue
            time.sleep(zzz)
            r = requests.get(self.__series_url + s.a['href'][10:],
                             headers=self.__h)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'lxml')
                isbns = self.__isbns(soup, stop_isbn, c=c+1)
        return isbns

    def __isbns(self, soup, stop_isbn, c=1):
        isbns = []
        for v in soup.find_all('li', class_='group__book'):
            d = v.find('div', class_='detail__title')
            r = requests.get(self.__base_url + d.a['href'], headers=self.__h)
            if r.status_code == 200:
                soup2 = BeautifulSoup(r.content, 'lxml')
                i = soup2.find('div', class_='detail__amazon').a['href'][36:46]
                if stop_isbn and i == stop_isbn:
                    return isbns
                print d.a.text, i
                isbns.append(i)
                time.sleep(5)
        isbns.reverse()
        if self.__has_next(soup):
            isbns = self.__get_next(soup, stop_isbn, c=c) + isbns
        return isbns

    def get_isbn(self, stop_isbn=None):
        if self.__base_url == self.__series_url:
            return None
        r = requests.get(self.__series_url, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            print self.__title(soup), self.__latest(soup)
            isbns = self.__isbns(soup, stop_isbn)
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
        stop_isbn = ""
        if t in isbn_dict:
            stop_isbn = isbn_dict[t][-1]
        v = isbn_inquiry(t).get_isbn(stop_isbn)
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

    titles = [u'ワンピース', u'鬼滅の刃', u'ブラッククローバー',
              u'ちはやふる', u'君に届け', u'あさひなぐ']
    update(isbn_dict, titles)

    with open(isbn_file, 'w') as f:
        f.write(json.dumps(isbn_dict, ensure_ascii=False).encode('utf-8'))
