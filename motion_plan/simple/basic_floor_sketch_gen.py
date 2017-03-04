from seq_pair02 import simulated_annealing, instance_generator
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from descartes.patch import PolygonPatch
import cPickle as pickle

if __name__ == '__main__':
    sa = simulated_annealing(instance_generator(40))
    sa.sim()
    with open('basic_01.dat', 'w') as f:
        pickle.dump(sa.result(), f)
    fig, ax = plt.subplots()
    polygons = [Polygon(p) for p in sa.result()]
    for p in polygons:
        patch = PolygonPatch(p, facecolor='#6699cc', alpha=0.5)
        ax.add_patch(patch)
    bd = cascaded_union(polygons)
    print bd.type
    patch = PolygonPatch(bd, facecolor='#6699cc', linewidth=3, alpha=0.5)
    ax.add_patch(patch)

    ax.set_aspect('equal')
    ax.autoscale()
    ax.margins(0.1)
    plt.show()
