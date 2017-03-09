# -*- coding: utf-8 -*-
import os
import shutil
import sys
from glob import glob
import zipfile
from PIL import Image
from tqdm import tqdm


args = sys.argv
target_string = '*.zip'
if len(args) == 2:
    target_string = args[1]

img_suffix = ".jpg.png.gif.jpeg"

fs, zs = [], []
for f in glob(target_string):
    print unicode(f, 'cp932', 'ignore')
    fs.append(f)
    with zipfile.ZipFile(f) as zf:
        fn, sn = os.path.splitext(f)
        ozf = zipfile.ZipFile(fn + "_1" + sn, 'w', zipfile.ZIP_DEFLATED)
        zs.append(fn + "_1" + sn)
        tl = []
        size = (1200, 800)
        for e in tqdm(zf.infolist()):
            fn, sn = os.path.splitext(e.filename)
            if sn not in img_suffix:
                continue
            with zf.open(e) as i:
                img = Image.open(i).convert('RGB')
                img.thumbnail(size)
                of = e.filename
                if sn != '.jpg':
                    of = fn + '.jpg'
                img.save(of, 'JPEG')
                tl.append(of)
                ozf.write(of)
        ozf.close()
        for t in tl:
            os.remove(t)

for f in fs:
    os.remove(f)
for z, f in zip(zs, fs):
    os.rename(z, f)
