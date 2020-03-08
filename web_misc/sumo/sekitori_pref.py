import os.path
import pickle
import time
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import japanmap as jp
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import requests
from tqdm import tqdm


def pref_check(pid):
    ranks, names = [], []
    url = 'http://www.sumo.or.jp/ResultRikishiData/search?pref_id=' + str(pid)
    headers = {'User-Agent': UserAgent().random}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        table = bs(r.content, 'lxml').find('table', class_='mdTable3')
        for th in table.find_all('th'):
            ranks.append(th.text.strip(" \n"))
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                names.append(td.text.strip(" \n"))
                break
    return list(zip(ranks, names))


def sumo_wrestler(enforce=False):
    sumo = []
    if enforce or not os.path.exists('sumo.pkl'):
        for i in tqdm(range(1, 48)):
            sumo.append(pref_check(i))
            time.sleep(1)
        with open('sumo.pkl', 'wb') as f:
            pickle.dump(sumo, f)
    else:
        with open('sumo.pkl', 'rb') as f:
            sumo = pickle.load(f)
    return sumo


def sekitori(sumo):
    seki = [[] for i in range(47)]
    for i in range(47):
        for r, p in sumo[i]:
            x = r[1:3]
            if x in u'横綱大関関脇小結前頭十両':
                if not seki[i]:
                    print('\n', jp.pref_names[i + 1])
                seki[i].append((r, p))
                print(r, p)
    return seki


def draw_pref_regions(dist, max_card, cmap):
    pts = jp.pref_points(jp.get_data())
    c = cmap(list(map(lambda c: c/max_card, dist)))
    for i in range(47):
        poly = plt.Polygon(pts[i], ec='k', fc=c[i], lw=0.5)
        plt.gca().add_patch(poly)
    plt.autoscale()


def draw_color_bar(max_card, cmap):
    sm = cm.ScalarMappable(cmap=cmap)
    sm._A = []
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes('right', size='2%', pad='1%')
    cbar = plt.colorbar(sm, cax=cax, ticks=np.linspace(0, 1, max_card+1))
    cbar.ax.set_yticklabels(range(max_card+1))


def draw_title(is_sekitori):
    fpath = '/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc'
    fp = FontProperties(fname=fpath)
    if is_sekitori:
        plt.gca().set_title(u'関取', fontproperties=fp, fontsize=14)
        plt.savefig('sumo_sekitori_pref.png', bbox_inches='tight')
    else:
        plt.gca().set_title(u'すべての力士', fontproperties=fp, fontsize=14)
        plt.savefig('sumo_pref.png', bbox_inches='tight')


def draw_prefs(sumo, is_sekitori=True):
    plt.clf()
    plt.gca().set_aspect('equal')
    plt.axis('off')

    dist = ([len(s) for s in sekitori(sumo)] if is_sekitori
            else [len(s) for s in sumo])
    max_card = max(dist)
    cmap = cm.Reds

    draw_pref_regions(dist, max_card, cmap)
    draw_color_bar(max_card, cmap)
    draw_title(is_sekitori)


if __name__ == '__main__':
    plt.figure(figsize=(12, 12))
    draw_prefs(sumo_wrestler())
    draw_prefs(sumo_wrestler(), is_sekitori=False)
