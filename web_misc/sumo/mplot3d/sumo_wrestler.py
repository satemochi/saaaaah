# -*- coding: utf-8 -*-
import os.path
import pickle
import time
from bs4 import BeautifulSoup as bs
import requests


def sekitori(sumo=None):
    if not sumo:
        sumo = sumo_wrestler()
    seki = [[] for i in range(47)]
    for i in range(47):
        for r, n, a in sumo[i]:
            x = r[1:3]
            if x in u'横綱大関関脇小結前頭十両':
                seki[i] = seki[i] + [(r, n, a)]
    return seki


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


def pref_check(pid):
    base = 'http://www.sumo.or.jp/ResultRikishiData/search?pref_id='
    ranks, names, affiliations = [], [], []
    r = requests.get(base + str(pid))
    if r.status_code == 200:
        table = bs(r.content, 'lxml').find('table', class_='mdTable3')
        for th in table.find_all('th'):
            ranks.append(th.text.strip(" \n"))
        for tr in table.find_all('tr'):
            name, _, affiliation = tr.find_all('td')
            names.append(name.text.strip(" \n"))
            affiliations.append(affiliation.text.strip(" \n"))
    return zip(ranks, names, affiliations)
