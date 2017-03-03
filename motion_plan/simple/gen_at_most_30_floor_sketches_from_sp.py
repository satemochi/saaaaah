from seq_pair02 import simulated_annealing, instance_generator
import cPickle as pickle
import os
from shapely.geometry import Polygon
from shapely.ops import cascaded_union


def extract_poly_coords(geom):
    if geom.type == 'Polygon':
        v = [list(p) for p in geom.exterior.coords[:]]
        exterior_coords = [list(s) for s in zip(v[:-1], v[1:])]
        interior_coords = []
        for i in geom.interiors:
            v = [list(p) for p in i.coords[:]]
            interior_coords += [list(s) for s in zip(v[:-1], v[1:])]
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return (exterior_coords, interior_coords)

if __name__ == '__main__':
    dump_dir = 'dat/'
    if not os.path.exists(dump_dir):
        os.mkdir(dump_dir)
    for i in range(1, 31):
        sa = simulated_annealing(instance_generator(40))
        sa.sim()
        if cascaded_union([Polygon(p) for p in sa.result()]).type != 'Polygon':
            continue
        with open(dump_dir + str(i).zfill(3) + '.dat', 'w') as f:
            pickle.dump(sa.result(), f)
