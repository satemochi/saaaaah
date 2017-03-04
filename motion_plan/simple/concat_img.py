import cv2
from glob import glob
import os

if __name__ == '__main__':
    outdir = 'cat_imgs/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    in1, in2 = glob('sp_img/*'), glob('vg_img/*')
    for img1, img2 in zip(in1, in2):
        i = cv2.imread(img1)
        j = cv2.imread(img2)
        cv2.imwrite(outdir + img2[7:10] + '-con.png', cv2.hconcat([i, j]))

