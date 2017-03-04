import cPickle as pickle
import os
import subprocess
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
from shapely.ops import cascaded_union


if __name__ == '__main__':
    if not os.path.exists('basic_01.dat'):
        subprocess.call('basic_floor_sketch.py', shell=True)
    with open('basic_01.dat', 'r') as f:
        o = pickle.load(f)
    fig, ax = plt.subplots()

    polygons = [Polygon(p) for p in o]
    for p in polygons:
        patch = PolygonPatch(p, facecolor='#6699cc', alpha=0.3)
        ax.add_patch(patch)

    boundary = cascaded_union(polygons)
    print boundary.type
    patch = PolygonPatch(boundary, facecolor='#6699cc', edgecolor='r',
                         linewidth=3, alpha=0.7, zorder=2)
    ax.add_patch(patch)

    ax.set_aspect('equal')
    ax.autoscale()
    ax.margins(0.1)
    plt.show()
