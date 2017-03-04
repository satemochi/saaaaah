import subprocess
import threading


def enjoy(s):
    subprocess.call(s, shell=True)


def ensmall(target):
    subprocess.call('..\ensmall_img.py', cwd=target, shell=True)


if __name__ == '__main__':
    scripts = ['kurage-bunch.py', 'tomochan.py', 'gangan-online.py',
               'tonarinoyj.py']
    threads = []
    for s in scripts:
        t = threading.Thread(target=enjoy, args=(s,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    resizes = ['adachito', 'barakamon', 'ebinachan', 'nanashino', 'nozaki',
               'onepanman', 'shakunetu', 'watashiga', 'realno']
    for t in resizes:
        ensmall(t)
