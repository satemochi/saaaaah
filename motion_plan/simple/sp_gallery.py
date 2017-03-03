from poly_voro import poly_voro
from ridge_graph import ridge_graph, get_st
import cPickle as pickle
from glob import glob
import os
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import matplotlib.pyplot as plt
import matplotlib.collections as mc


def draw(pv, sp_ridges, fname):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    patch = PolygonPatch(floor_sketch, facecolor='#6699cc', linewidth=2)
    ax.add_patch(patch)
    ax.add_collection(mc.LineCollection(pv.ridges))
    ax.add_collection(mc.LineCollection(sp_ridges, colors='r', linewidth=2))
    ax.autoscale()
    ax.margins(0.1)
    plt.savefig(fname, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    out_dir = 'sp_img/'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for d in glob('dat/*.dat'):
        fname = out_dir + d[4:-4] + '-sp.png'
        print fname
        if os.path.exists(fname):
            continue
        with open(d, 'r') as f:
            o = pickle.load(f)
        floor_sketch = cascaded_union([Polygon(p) for p in o])
        pv = poly_voro(floor_sketch)
        rg = ridge_graph(pv.ridges)
        s, t = get_st(pv.ridges)
        draw(pv, rg.get_sp_ridges(s, t), fname)
