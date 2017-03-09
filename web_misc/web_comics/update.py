# -*- coding: utf-8 -*-
import subprocess
import threading
from glob import glob
import os
import codecs


def enjoy(s):
    subprocess.call(s, shell=True)


def ensmall(target, fname):
    print target
    subprocess.call(('..\ensmall_img.py ' + fname).encode('shift-jis'),
                    cwd=target, shell=True)


def resize_check():
    if os.path.exists('ghostdriver.log'):
        os.remove('ghostdriver.log')
    targets = []
    for logs in glob('*.log'):
        with codecs.open(logs, 'r', 'utf-8') as f:
            lines = f.read().splitlines()
        for l in lines:
            dname, fname = l.split(' ')[-1].split('/')
            targets.append([dname, fname])
    return targets


def remove_logs():
    for f in glob('*.log'):
        os.remove(f)


if __name__ == '__main__':
    remove_logs()
    scripts = ['kurage-bunch.py', 'tomochan.py', 'gangan-online.py',
               'tonarinoyj.py']
    threads = []
    for s in scripts:
        t = threading.Thread(target=enjoy, args=(s,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    resizes = resize_check()
    for t, f in resizes:
        ensmall(t, f)
