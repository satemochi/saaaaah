# -*- coding: utf-8 -*-
import json
import os
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import requests
from tqdm import tqdm


class booklog():
    def __init__(self):
        self.__base_url = 'http://booklog.jp/item/1/'
        self.__h = {'User-Agent': UserAgent().random}

    def __u(self, soup):
        u = soup.find('li', class_='users')
        return int(u.span.text) if u is not None else 0

    def __rat(self, soup):
        u = soup.find('li', class_='rating')
        return float(u.span.text) if u is not None else 0

    def __rev(self, soup):
        u = soup.find('li', class_='reviews')
        return int(u.span.text) if u is not None else 0

    def get(self, isbn):
        r = requests.get(self.__base_url + isbn, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            return [self.__u(soup), self.__rat(soup), self.__rev(soup)]
        return [0, 0.0, 0]


class bookmeter():
    def __init__(self):
        self.__base_url = 'http://bookmeter.com/b/'
        self.__h = {'User-Agent': UserAgent().random}

    def __u(self, soup):
        u = soup.find('span', class_='readers')
        return int(u.text[:-2]) if u is not None else 0

    def get(self, isbn):
        r = requests.get(self.__base_url + isbn, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            return self.__u(soup)
        return 0


def request(title):
    with open('isbn2.json', 'r') as f:
        isbn_dict = json.load(f)
    if title not in isbn_dict:
        return None
    columns = ['booklog', 'bl_ratings', 'bl_reviews', 'bookmeter']
    rows = []
    print title
    for isbn in tqdm(isbn_dict[title]):
        rows.append(booklog().get(isbn) + [bookmeter().get(isbn)])
        time.sleep(3)
    index = range(1, len(isbn_dict[title]) + 1)
    df = pd.DataFrame(rows, index=index, columns=columns)
    df.index.name = 'vol'
    return df


def get_df(title):
    csv = title + '.csv'
    if os.path.exists(csv):
        return pd.read_csv(csv, index_col='vol', encoding='utf-8')
    else:
        df = request(title)
        if df is not None:
            df.to_csv(csv, encoding='utf-8')
        return df


def draw(df, title):
    ax = df[['booklog', 'bookmeter']].plot(kind='bar', rot=0)
    ax2 = ax.twinx()
    ax2.plot(df[['bl_ratings']].values, c='r')
    ax2.set_ylim([0, 6])

    xtic = [0] + range(4, len(df)+1, 5)
    plt.xticks(xtic, [str(i+1) for i in xtic])

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc', size=12)
    plt.title(title, fontproperties=fp)

if __name__ == '__main__':
    titles = [u'ワンピース', u'ナルト', u'ブラッククローバー', u'鬼滅の刃',
              u'ちはやふる', u'君に届け']
    for t in titles:
        if os.path.exists(t + '.png'):
            continue
        df = get_df(t)
        if df is None:
            quit()
        draw(df, t)
        plt.savefig(t + '.png', bbox_inches='tight')
        plt.close()
