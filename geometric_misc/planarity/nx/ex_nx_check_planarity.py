from itertools import izip
import math
from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms.planarity import check_planarity
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, Point


def get_cycle(g, mi=None):
    cb = nx.cycle_basis(g)
    if not mi or mi >= len(cb):
        argmax = lambda array: max(izip(array, xrange(len(array))))[1]
        mi = argmax([len(c) for c in cb])
    return cb[mi]


def fix_outer_cycle_pos(g, cycle_vertices):
    rad = 2 * math.pi / len(cycle_vertices)
    for i, v in enumerate(cycle_vertices):
        g.node[v]['coord'] = (math.cos(rad * i), math.sin(rad * i))


def fix_all_pos(g):
    # building coefficient-matrices for xy-coordinates of the unfixed vertices
    A, Bx, By = [], [], []
    for v in g.nodes():
        a = [0] * nx.number_of_nodes(g)
        bx, by = 0, 0
        if 'coord' in g.node[v]:    # a fixed vertex which is constant
            a[v] = 1
            bx = g.node[v]['coord'][0]
            by = g.node[v]['coord'][1]
        else:
            a[v] = len(g[v])
            for n in g[v]:      # for neighbors
                a[n] = -1       # to be the barycenter constraint
        A.append(a)
        Bx.append(bx)
        By.append(by)
    # solving systems of linear equations
    xcoords = np.linalg.solve(A, Bx)
    ycoords = np.linalg.solve(A, By)
    # asigning coordinates
    coords = zip(xcoords, ycoords)
    for v, coord in enumerate(coords):
        g.node[v]['coord'] = coord
    return coords


def centroidal(pts, cycle):
    maxd = 0.0
    b = Polygon([pts[v] for v in cycle])
    vor = Voronoi(pts)
    for i in range(len(pts) - 3):
        if i in cycle:
            continue
        poly = [vor.vertices[v] for v in vor.regions[vor.point_region[i]]]
        cell = b.intersection(Polygon(poly))
        p = Point(pts[i])
        pts[i] = cell.centroid.coords[0]
        d = p.distance(Point(pts[i]))
        if maxd < d:
            maxd = d
    return maxd


def relax(pos, cycle):
    n_rounds, d_threshold  = 200, 0.001
    pos = pos + [[100, 100], [100, -100], [-100, 0]]
    for i in range(n_rounds):
        if centroidal(pos, cycle) < d_threshold:
            break
    return pos[:-3]


def getpos(g, cid=0):
    c = get_cycle(g, cid)
    fix_outer_cycle_pos(g, c)
    return relax(fix_all_pos(g), c)


if __name__ == '__main__':
    g = nx.chvatal_graph()
    pos = getpos(g)
    nx.draw(g, pos, alpha=0.25)

    is_planar, certificate = check_planarity(g, counterexample=True)
    if is_planar:
        print 'planar'
    else:
        print 'non planar'
        nx.draw_networkx(certificate, pos, node_color='#99ff99')

    plt.gca().set_aspect('equal')
    plt.savefig('ex_nx_check_planarity_1.png', bbox_inches='tight')
    plt.show()
