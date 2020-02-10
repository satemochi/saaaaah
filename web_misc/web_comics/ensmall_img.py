import os
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
    print(f)
    fs.append(f)
    with zipfile.ZipFile(f) as zf:
        fn, sn = os.path.splitext(f)
        ozf = zipfile.ZipFile(fn + "_1" + sn, 'w', zipfile.ZIP_DEFLATED)
        zs.append(fn + "_1" + sn)
        tl = []
        size = (1200, 800)
        for e in tqdm(zf.infolist()):
            fn, sn = os.path.splitext(e.filename)
            if len(sn) < 1 or sn not in img_suffix or '__' in fn:
                continue
            of = e.filename.split('/')[-1]
            with zf.open(e) as i:
                img = Image.open(i).convert('RGB')
                img.thumbnail(size)
                if sn != '.jpg':
                    of = fn.split('/')[-1] + '.jpg'
                img.save(of, format='JPEG')
                tl.append(of)
                ozf.write(of)
        ozf.close()
        for t in tl:
            os.remove(t)

for f in fs:
    os.remove(f)
for z, f in zip(zs, fs):
    os.rename(z, f)
