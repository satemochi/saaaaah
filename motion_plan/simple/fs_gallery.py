from poly_voro import poly_voro
import cPickle as pickle
from glob import glob
import os
import subprocess
from shapely.geometry import Polygon
from shapely.ops import cascaded_union


if __name__ == '__main__':
    out_dir = 'fs_img/'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for d in glob('dat/*.dat'):
        fname = out_dir + d[4:-3] + 'png'
        print fname
        if os.path.exists(fname):
            continue
        with open(d, 'r') as f:
            o = pickle.load(f)
        floor_sketch = cascaded_union([Polygon(p) for p in o])
        pv = poly_voro(floor_sketch)
        pv.savefig(fname)
