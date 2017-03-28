# -*- coding: utf-8 -*-
import json
import os
import random
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import requests
from tqdm import tqdm


class amazon():
    def __init__(self, isbn):
        self.__base_url = 'http://www.amazon.co.jp/dp/' + isbn
        self.__h = {'User-Agent': UserAgent().random}

    def __rat(self, soup):
        s = soup.find('div', id='summaryStars')
        return float(s.a.i.span.text.split(' ')[1]) if s is not None else 0.0

    def __rev(self, soup):
        s = soup.find('div', id='summaryStars')
        return int(s.a.text.split('\n')[2]) if s is not None else 0.0

    def __his(self, soup):
        s = soup.find_all('tr', class_='a-histogram-row')
        return [int(tr.find_all('td')[2].text) for tr in s] if s else []

    def get(self):
        r = requests.get(self.__base_url, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            return [self.__rat(soup), self.__rev(soup)] + self.__his(soup)
        return 0


def request(title, zzz=120):
    with open('isbn2.json', 'r') as f:
        isbn_dict = json.load(f)
    columns = ['a_ratings', 'a_reviews', u'☆5', u'☆4', u'☆3', u'☆2', u'☆1']
    rows = []
    print title
    for isbn in tqdm(isbn_dict[title]):
        rows.append(amazon(isbn).get())
        time.sleep(zzz + random.randint(0, 60))

    index = range(1, len(isbn_dict[title]) + 1)
    df = pd.DataFrame(rows, index=index, columns=columns)
    df.index.name = 'vol'
    return df


if __name__ == '__main__':
    titles = [u'ワンピース', u'ナルト', u'ブラッククローバー',
              u'それでも町は廻っている', u'鬼滅の刃']
    for t in titles:
        csv = t + '-a2.csv'
        if not os.path.exists(csv):
            df = request(t)
            df.to_csv(csv, encoding='utf-8')
