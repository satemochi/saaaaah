from glob import glob
import os
import shutil
import time
from zipfile import ZipFile, ZIP_DEFLATED
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


def dl_img(url, fname, headers):
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        with open(fname, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def get_imgs(url, wait_sec=30):
    files = []
    headers = {'User-Agent': UserAgent().random}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        ma = BeautifulSoup(r.content, 'lxml').find('div', id='manga_area')
        for img in ma.findAll('img'):
            if '.jpg' in img['src']:
                dl_img(url + img['src'], img['src'][4:], headers)
                files.append(img['src'][4:])
                time.sleep(wait_sec)
    return files


def archiving(imgs, title, chap):
    if len(imgs) != 0:
        with ZipFile(chap + '.zip', 'w', ZIP_DEFLATED) as zf:
            for img in imgs:
                zf.write(img)
        for img in imgs:
            os.remove(img)
        shutil.move(chap + '.zip', title)


def get_chaps(title, chaps):
    base_url = 'http://www.kurage-bunch.com/manga'
    for chap in chaps:
        print title, str(chap)
        if os.path.exists(title + '/' + str(chap) + '.zip'):
            continue
        imgs = get_imgs(base_url + "/" + title + "/" + str(chap).zfill(2) + "/")
        archiving(imgs, title, str(chap))


def current_chap(title):
    if not os.path.exists(title):
        os.mkdir(title)
        return 0
    c, _ = os.path.splitext(os.path.basename(max(glob(title + '/*'))))
    return int(c) + 1


def latest_chap(title, cchap):
    lchap = 0
    r = requests.get('http://www.kurage-bunch.com/manga/' + title)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        for i in soup.find_all('ul', id='backnumber'):
            lc = int(i.li.a.text)
            if lc >= cchap:
                lchap = lc
                break
    return lchap + 1


def update(titles):
    for title in titles:
        c = current_chap(title)
        l = latest_chap(title, c)
        print title, c, l
        get_chaps(title, range(c, l))


if __name__ == '__main__':
    titles = ['yamashoku', 'shojoshumatsu', 'orgasm', 'youkai']
    update(titles)
