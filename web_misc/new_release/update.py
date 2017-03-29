# -*- coding: utf-8 -*-
from datetime import datetime
import random
import os.path
import sqlite3
import time
import requests
import requests.packages.urllib3
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from fake_useragent import UserAgent


def set_up():
    conn = sqlite3.connect('comics.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return (conn, c)


def tear_down(conn):
    conn.commit()
    conn.close()


def get_target(c):
    sql = "SELECT id, title, author, publish_date, last_update, volume, \
           isbn, next_date FROM comics"
    return c.execute(sql).fetchall()


def is_recently_updated(last_d):
    if last_d is None:
        return False
    td = datetime.now()
    ud = datetime.strptime(last_d, '%Y/%m/%d')
    if (td - ud).days < 1:
        return True
    return False


def get_publisher_and_isbn(soup):
    pub, isbn = None, None
    target_div = soup.find('div', id="detail_bullets_id")
    if target_div is not None:
        for div in target_div.findAll('div', class_='content'):
            for li in div.findAll('li'):
                if u"出版社" in li.text:
                    pub = li.text.split(' ')[1]
                elif u"ISBN-10" in li.text:
                    isbn = li.text[9:]
    return (pub, isbn)


def get_stars(soup):
    stars, reviewers = None, None
    sdiv = soup.find('div', id="summaryStars")
    if sdiv is not None:
        stars = float(sdiv.a.i.span.text.split(' ')[1])
        reviewers = int(sdiv.a.text.split('\n')[2])
    return (stars, reviewers)


def get_reviews(soup):
    reviews = ""
    for div in soup.findAll('div', class_="a-row a-spacing-small"):
        d = div.find('div', class_='a-section')
        if d is not None:
            if d.span is None:
                reviews = reviews + d.text
            else:
                reviews = reviews + '\n' + d.span.text + '\n'
    return reviews


def detail_info(url):
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(r.content, 'lxml')
    pub, isbn = get_publisher_and_isbn(soup)
    stars, reviewers = get_stars(soup)
    reviews = get_reviews(soup)
    return (pub, isbn, stars, reviews, reviewers)


def write_amazon_info(c, url, cid):
    sql = "UPDATE comics SET publisher = ?, \
           isbn = ?, stars = ?, reviews = ?, \
           reviewers = ? WHERE id LIKE ?"
    pub, isbn, star, review, reviewer = detail_info(url)
    if pub is None:
        print "fail to accessing Amazon"
    else:
        c.execute(sql, (pub, isbn, star, review, reviewer, cid))


def amazon(c, isbn, path, cid):
    if isbn is not None:
        url = 'https://www.amazon.co.jp/dp/' + isbn
        write_amazon_info(c, url, cid)
    else:
        url = 'http://alert.shop-bell.com' + path
        r = requests.get(url, headers={'User-Agent': UserAgent().random})
        soup = BeautifulSoup(r.content, 'lxml')
        reserve_url = ""
        for div in soup.findAll('div', class_="itemdiv media"):
            for d in div.findAll('div'):
                if d.span is None or d.span.text is None:
                    continue
                if d.span.text == u"発売済み最新刊":
                    url = 'https://www.amazon.co.jp/dp/' + d.a['href'][10:-1]
                    write_amazon_info(c, url, cid)
                    return
                elif d.span.text == u'発売予定':
                    reserve_url = 'https://www.amazon.co.jp/dp/' + \
                                   d.a['href'][10:-1]
        if reserve_url != "":
            write_amazon_info(c, reserve_url, cid)


def get_tab(title, author):
    data = {'safesearch': '1', 'Books': '1', 'Title': title, 'Author': author}
    r = requests.get('http://alert.shop-bell.com/search/', data)
    soup = BeautifulSoup(r.content, "lxml")
    return soup.find('table', class_="table span12 reflow")


def set_vol_and_pubdate(c, soup, cvol, cid):
    info = soup.find('td', class_="srpLatest").text
    if info != u"未発売":
        vol = info.split(u"巻")[0]
        pd = info.split(u"巻")[1].split(" ")[0]
        pub_date = pd[:4] + "/" + pd[5:7] + "/" + pd[8:-1]
        nd = soup.find('td', class_="srpNext").span.text
        if u'未定' in nd:
            nd = u'未定'
        elif u'予定' in nd:
            nd = nd.split(' ')[0]
            nd = nd[:4] + "/" + nd[5:7] + "/" + nd[8:-1]
        elif u'予想' in nd:
            nd = nd.split(' ')[0][1:-1]
            nd = nd[:4] + "/" + nd[5:7] + "/" + nd[8:-1]
        c.execute("UPDATE comics SET next_date = ?  WHERE id LIKE ?",
                  (nd, cid))
        if int(vol) != cvol:
            c.execute("UPDATE comics SET volume = ?, publish_date = ? \
                       WHERE id LIKE ?", (vol, pub_date, cid))
            return True
        else:
            return False
    return False


def set_lastdate(c, cid):
    sql = "UPDATE comics SET last_update = ? WHERE id LIKE ?"
    c.execute(sql, (datetime.now().strftime('%Y/%m/%d'), cid))


def update():
    conn, c = set_up()
    for cid, title, author, pub_d, last_d, vol, isbn, next_d, in get_target(c):
        if is_recently_updated(last_d):
            continue
        print cid, title, vol, pub_d, next_d, last_d
        set_lastdate(c, cid)
        for tr_ in get_tab(title, author).tbody.findAll('tr'):
            td_ = tr_.find('td', class_="urlcol srpTitle")
            if SequenceMatcher(None, title, td_.a.text).ratio() < 0.75:
                continue
            sql = "UPDATE comics SET url_id = IfNull(url_id, ?) \
                   WHERE id LIKE ?"
            c.execute(sql, (td_.a['href'][7:-1], cid))
            new_released = set_vol_and_pubdate(c, tr_, vol, cid)
            if new_released:
                amazon(c, None, td_.a['href'], cid)
            else:
                amazon(c, isbn, td_.a['href'], cid)
            time.sleep(random.randint(120, 180))
            break
        conn.commit()
    tear_down(conn)


if __name__ == '__main__':
    update()
