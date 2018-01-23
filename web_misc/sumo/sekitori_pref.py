# -*- coding: utf-8 -*-
import os.path
import pickle
import time
from bs4 import BeautifulSoup as bs
import japanmap as jp
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.font_manager import FontProperties
import requests


def pref_check(pid):
    base = 'http://www.sumo.or.jp/ResultRikishiData/search?pref_id='
    ranks, names = [], []
    r = requests.get(base + str(pid))
    if r.status_code == 200:
        table = bs(r.content, 'lxml').find('table', class_='mdTable3')
        for th in table.find_all('th'):
            ranks.append(th.text.strip(" \n"))
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                names.append(td.text.strip(" \n"))
                break
    return zip(ranks, names)


def sumo_wrestler(enforce=False):
    sumo = []
    if enforce or not os.path.exists('sumo.pkl'):
        for i in range(1, 48):
            sumo.append(pref_check(i))
            time.sleep(1)
        with open('sumo.pkl', 'wb') as f:
            pickle.dump(sumo, f)
    else:
        with open('sumo.pkl', 'rb') as f:
            sumo = pickle.load(f)
    return sumo


def get_japanmap():
    with open('japan.p2.pkl', 'rw') as f:
        return pickle.load(f)


def color_mag(sumo):
    a = [len(s) for s in sumo]
    max_, min_ = max(a), min(a)
    return cm.hot(map(lambda c: 1-float(c - min_)/(max_+1.0), a))


def sekitori(sumo):
    seki = [[] for i in range(47)]
    for i in range(47):
        for r, p in sumo[i]:
            x = r[1:3]
            if x in u'横綱大関関脇小結前頭十両':
                seki[i] = seki[i] + [(r, p)]
    for i, s in enumerate(seki):
        if s:
            print jp.pref_names[i + 1]
            for r, p in s:
                print r, p
            print
    return seki


def draw_prefs(sumo, is_sekitori=True):
    if is_sekitori:
        sumo = sekitori(sumo_wrestler())
    pts = jp.pref_points(get_japanmap())
    c = color_mag(sumo)
    for i in range(47):
        poly = plt.Polygon(pts[i], ec='k', fc=c[i], lw=0.5)
        plt.gca().add_patch(poly)

    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.autoscale()
    fpath = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
    fp = FontProperties(fname=fpath)
    if is_sekitori:
        plt.gca().set_title(u'関取', fontproperties=fp)
        plt.savefig('sumo_sekitori_pref.png', bbox_inches='tight')
    else:
        plt.gca().set_title(u'すべての力士', fontproperties=fp)
        plt.savefig('sumo_pref.png', bbox_inches='tight')


if __name__ == '__main__':
    draw_prefs(sumo_wrestler())
    draw_prefs(sumo_wrestler(), is_sekitori=False)
