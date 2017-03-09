import logging
import os
import shutil
import signal
import time
from glob import glob
from zipfile import ZipFile, ZIP_DEFLATED
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains


def current_chap(title):
    if not os.path.exists(title):
        os.mkdir(title)
        return 0
    return max([int(os.path.splitext(os.path.basename(x))[0])
                for x in glob(title + '/*.zip')])


def get_info(title):
    links = []
    r = requests.get('http://www.tonarinoyj.jp/manga/' + title)
    if r.status_code == 200:
        current = current_chap(title)
        soup = BeautifulSoup(r.content, 'lxml')
        for li in soup.find('div', class_='single-backnumber').findAll('li'):
            chap = int(li.a.text[:-4])
            if chap == current:
                break
            elif chap > current:
                links.append((chap, li.a['href']))
    return links


def move_to_first(driver, pages=2, wait_sec=1):
    for i in range(pages):
        ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(wait_sec)


def get_pages(driver):
    elem = driver.find_element_by_class_name('viewer-heder-pager')
    pages = elem.find_elements_by_tag_name('span')[1]
    return (int(pages.get_attribute('innerHTML').split('/')[1]) + 1) / 2 + 1


def setUp(url, wait_sec=30):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = UserAgent().random
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_window_size(1114, 800)
    driver.get(url)
    time.sleep(wait_sec)
    pages = get_pages(driver)
    move_to_first(driver, pages + 2)
    return (driver, pages)


def screenshot(driver, title, pages=8, wait_sec=10):
    files = []
    for i in range(pages):
        fname = title + "-" + str(i).zfill(2) + '.png'
        driver.save_screenshot(fname)
        ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
        files.append(fname)
        time.sleep(wait_sec)
    return files


def archiving(files, title, chap):
    if len(files) != 0:
        zfname = str(chap) + '.zip'
        with ZipFile(zfname, 'w', ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(f)
        for f in files:
            os.remove(f)
        shutil.move(zfname, title)
        logging.critical(title + "/" + zfname)


def tearDown(driver):
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()


def snapshot(title):
    for chap, url in get_info(title):
        if not os.path.exists(title + '/' + str(chap) + '.zip'):
            driver, pages = setUp(url)
            print title, chap, pages
            files = screenshot(driver, title, pages)
            archiving(files, title, chap)
            tearDown(driver)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d',
                        filename='tonarinoyj.log', level=logging.CRITICAL)
    titles = ['onepanman', 'shakunetu', 'ebinachan']
    for title in titles:
        print title
        snapshot(title)
