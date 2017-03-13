# -*- coding: utf-8 -*-
import json
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from fake_useragent import UserAgent
import os
from matplotlib.font_manager import FontProperties

def users(soup):
    u = soup.find('li', class_='users')
    return int(u.span.text) if u is not None else 0

def rating(soup):
    u = soup.find('li', class_='rating')
    return float(u.span.text) if u is not None else 0

def reviews(soup):
    u = soup.find('li', class_='reviews')
    return int(u.span.text) if u is not None else 0

def get(isbn):
    r = requests.get('http://booklog.jp/item/1/' + isbn,
                     headers={'User-Agent': UserAgent().random})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        return (users(soup), rating(soup), reviews(soup))
    return (0, 0.0, 0)

def enjoy(title):
    csv = title + '.csv'
    if os.path.exists(csv):
        return pd.read_csv(csv, index_col='vol', encoding='utf-8')
    else:
        with open('isbn.json', 'r') as f:
            data = json.load(f)

        columns =['users', 'ratings', 'reviews']
        rows = []
        for i, isbn in enumerate(data[title], start=1):
            print i, isbn
            rows.append(get(isbn))
            time.sleep(3)
        df = pd.DataFrame(rows, index=range(1, len(data[title]) + 1),
                          columns=columns)
        df.index.name = 'vol'
        df.to_csv(csv, encoding='utf-8')
        return df

if __name__ == '__main__':
#    title = u'ONE PIECE'
#    title = u'ブラッククローバー'
#    title = u'HUNTER X HUNTER'
#    title = u'ちはやふる'
#    title = u'NARUTO -ナルト-'
    title = u'BLEACH'
    df = enjoy(title)

    ax = df[['users', 'reviews']].plot(kind='bar', rot=0)
    ax2 = ax.twinx()
    ax2.plot(df[['ratings']].values, c='r')
    ax2.set_ylim([0, 6])
    xtic = [0] + range(4, len(df)+1, 5)
    plt.xticks(xtic, [str(i+1) for i in xtic])

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\DFJHSGW5.ttc', size=12)
    plt.title(title, fontproperties=fp)
    plt.show()



