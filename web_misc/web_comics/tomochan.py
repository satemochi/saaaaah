from glob import glob
import os
from os.path import exists, splitext, basename
import shutil
import time
import requests
from bs4 import BeautifulSoup


def current_chap(d):
    if not exists(d):
        os.mkdir(d)
        return 1
    return int(splitext(basename(max(glob(d + '*.jpg'))))[0]) + 1


def latest_chap(title):
    lchap = 1
    r = requests.get('http://sai-zen-sen.jp/comics/twi4/' + title)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        lchap += int(soup.find('nav', id='backnumbers').li.a.text[-3:])
    return lchap


def get_imgs(title, s, e, wait_sec=30):
    for chap in range(s, e):
        msg = title[:-1] + "\t" + str(chap)
        fname = str(chap).zfill(4) + '.jpg'
        data = 'http://sai-zen-sen.jp/comics/twi4/' + title + 'works/' + fname
        r = requests.get(data, stream=True)
        if r.status_code == 200:
            with open(title + fname, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            time.sleep(wait_sec)


def update(title):
    s = current_chap(title)
    e = latest_chap(title)
    msg = title[:-1] + ": current:" + str(s - 1) + \
            ", latest:" + str(e - 1) + ", gap:" + str(e - s)
    print msg
    get_imgs(title, s, e)

if __name__ == '__main__':
    titles = ['tomochan/', 'bungakushoujo/', 'honeycome/', 'moutele/', 
              'marian/']
    for t in titles:
        update(t)
