# -*- coding: utf-8 -*-
from wc_example1 import morphological_analysis, draw_wordcloud
import json
import os
import random
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import matplotlib.pyplot as plt
import requests


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

    def __tex(self, soup):
        reviews = ""
        for div in soup.find_all('div', class_='a-row a-spacing-small'):
            d = div.find('div', class_='a-section')
            if d is not None:
                reviews += '\n' + d.span.text + '\n' if d.span else d.text
        return reviews

    def __his(self, soup):
        s = soup.find_all('tr', class_='a-histogram-row')
        return [int(tr.find_all('td')[2].text) for tr in s] if s else []

    def get(self):
        r = requests.get(self.__base_url, headers=self.__h)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            return [self.__rat(soup), self.__rev(soup), self.__tex(soup)] + \
                    self.__his(soup)
        return 0


def request(title, isbn_dict, zzz=120):
    print title
    for i, isbn in enumerate(isbn_dict[title], start=1):
        info = amazon(isbn).get()
        draw_wordcloud(morphological_analysis(info[2]))
        plt.axis('off')
        plt.savefig(title + '/' + str(i).zfill(3) + '.png',
                    bbox_inches='tight', dpi=200)
        plt.close()
        time.sleep(zzz + random.randint(0, 60))


if __name__ == '__main__':
    with open('isbn2.json', 'r') as f:
        isbn_dict = json.load(f)
    titles = [u'ワンピース']

    for t in titles:
        if not os.path.exists(t):
            os.mkdir(t)
        request(t, isbn_dict)
