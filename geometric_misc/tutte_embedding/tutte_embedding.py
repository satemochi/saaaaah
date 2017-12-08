from itertools import izip
import math
import sys
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, Point


class tutte_embedding:
    def __init__(self, g):
        self.__pos = [(sys.maxint, sys.maxint)] * nx.number_of_nodes(g)
        self.__rpos = []
        self.__embedding(g)

    def pos(self):
        return {v: coord for v, coord in enumerate(self.__pos)}

    def rpos(self):
        return {v: coord for v, coord in enumerate(self.__rpos)}

    def __argmax(self, array):
        return max(izip(array, xrange(len(array))))[1]

    def __get_cycle(self, g, mi=None):
        cb = nx.cycle_basis(g)
        if not mi or mi >= len(cb):
            mi = self.__argmax([len(c) for c in cb])
        return cb[mi]

    def __fix_outer_cycle_pos(self, cycle_vertices):
        rad = 2 * math.pi / len(cycle_vertices)
        for i, v in enumerate(cycle_vertices):
            self.__pos[v] = (math.cos(rad * i), math.sin(rad * i))

    def __fix_all_pos(self, g):
        # building coefficient-matrices
        A, Bx, By = [], [], []
        for v in g.nodes():
            a = [0] * nx.number_of_nodes(g)
            bx, by = 0, 0
            if sys.maxint not in self.__pos[v]:     # a fixed vertex
                a[v] = 1
                bx = self.__pos[v][0]
                by = self.__pos[v][1]
            else:
                a[v] = len(g[v])
                for n in g[v]:  # for neighbors
                    a[n] = -1   # to be barycenter-constraints
            A.append(a)
            Bx.append(bx)
            By.append(by)
        # solving systems of linear equations
        xcoords = np.linalg.solve(A, Bx)
        ycoords = np.linalg.solve(A, By)
        # asigning coordinates
        self.__pos = zip(xcoords, ycoords)

    def __centroidal(self, pts, cycle):
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

    def __relax(self, cycle):
        n_rounds, d_threshold = 200, 0.001
        pos = self.__pos + [(100, 100), (100, -100), (-100, 0)]
        for i in range(n_rounds):
            if self.__centroidal(pos, cycle) < d_threshold:
                break
        return pos[:-3]

    def __embedding(self, g):
        c = self.__get_cycle(g)
        self.__fix_outer_cycle_pos(c)
        self.__fix_all_pos(g)
        self.__rpos = self.__relax(c)


def __draw(g, ax=None, title=None, pos=None):
    if not ax:
        ax = plt.gca()
    nx.draw_networkx(g, pos=pos, ax=ax, node_color='g',
                     with_labels=False, node_size=20)
    if pos:
        pts = pos.values()
        pts += [[100, 100], [100, -100], [-100, 0]]
        voronoi_plot_2d(Voronoi(pts), ax=ax, show_vertices=False,
                        line_alpha=0.25)
    if title:
        ax.set_title(title)
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_axis_off()
    ax.set_aspect('equal')


if __name__ == '__main__':
    fname, g = 'tutte3.png', nx.tutte_graph()
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))

    te = tutte_embedding(g)
    __draw(g, ax1, 'ordinary Tutte\'s embedding', te.pos())
    __draw(g, ax2, 'centroidal Voronoi relaxation', te.rpos())

#    plt.savefig(fname, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
