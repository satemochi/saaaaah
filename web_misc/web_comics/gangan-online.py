import logging
import os
import signal
import shutil
import time
from zipfile import ZipFile, ZIP_DEFLATED
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent


def get_chaplink(title):
    base = 'http://www.ganganonline.com'
    content_path = '/contents/'
    r = requests.get(base + content_path + title)
    targets = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        for d in soup.find_all('div', class_='gn_detail_story_list'):
            chap = d.find('li', class_='gn_detail_story_list_ttl').text
            link = d.find('li', class_='gn_detail_story_btn').a['href'][5:]
            if 'void' in link:
                continue
            targets.append((chap.split(' ')[0][1:-1], base + link))
    return targets


def exists(title, chap):
    if os.path.exists(title) and os.path.exists(title + "/" + chap + '.zip'):
        return True
    return False


def set_up(url, wait_sec=10):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = UserAgent().random
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    reduction_ratio = 0.75
    driver.set_window_size(948 * 2 * reduction_ratio, 1326 * reduction_ratio)
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(wait_sec)
    elem = driver.find_element_by_id('pageSliderCounter')
    pages = int((int(elem.text.split('/')[1]) + 1) / 2)
    return (driver, pages)


def move_to_first(driver, pages=16):
    for i in range(pages):
        ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(1)


def screenshot(driver, title, pages=16, wait_sec=10):
    move_to_first(driver, pages=pages+3)
    files = []
    for i in range(pages):
        fname = title + '-' + str(i).zfill(2) + '.png'
        driver.save_screenshot(fname)
        ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
        files.append(fname)
        time.sleep(wait_sec)
    return files


def archive(files, title, chap):
    if len(files) != 0:
        zfname = chap + '.zip'
        with ZipFile(zfname, 'w', ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(f)
        for f in files:
            os.remove(f)
        if not os.path.exists(title):
            os.mkdir(title)
        shutil.move(zfname, title)
        logging.critical(title + "/" + zfname)


def tear_down(driver):
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()


def snapshot(title):
    targets = get_chaplink(title)
    for chap, link in targets:
        if not exists(title, chap):
            driver, pages = set_up(link)
            print title, chap, pages
            files = screenshot(driver, title, pages)
            archive(files, title, chap)
            tear_down(driver)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d',
                        filename='gangan-online.log', level=logging.CRITICAL)
    titles = ['watashiga', 'adachito', 'nozaki', 'nanashino', 'barakamon',
              'realno']
    for title in titles:
        print title
        snapshot(title)
