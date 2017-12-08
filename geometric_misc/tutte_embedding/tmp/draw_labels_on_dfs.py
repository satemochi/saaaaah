from itertools import izip
import math
from operator import add
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

#    def __get_cycle(self, g, mi=None):
    def __get_cycle(self, g, mi=3):
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
    nx.draw_networkx(g, pos=pos, ax=ax, node_color='orange',
                     with_labels=True, node_size=200)
    if title:
        ax.set_title(title)
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_axis_off()
    ax.set_aspect('equal')


def non_recursive_dfs(g):
    visited = [False] * nx.number_of_nodes(g)
    for v in g.nodes():
        if not visited[v]:
            yield v
            visited[v] = True
            stack = [(v, iter(g[v]))]
            while stack:
                parent, children = stack[-1]
                try:
                    child = next(children)
                    if not visited[child]:
                        yield child
                        visited[child] = True
                        stack.append((child, iter(g[child])))
                except StopIteration:
                    stack.pop()


def rdfs(g, v, visited):
    if not visited[v]:
        yield v
        visited[v] = True
        for w in iter(g[v]):
            for x in rdfs(g, w, visited):
                yield x


def recursive_dfs(g):
    visited = [False] * nx.number_of_nodes(g)
    for v in g.nodes():
        for x in rdfs(g, v, visited):
            yield x


def __draw_labels(g, ax=None, labels=None, pos=None):
    if not labels or not pos:
        return
    if not ax:
        ax = plt.gca()

    order = [0] * nx.number_of_nodes(g)
    for i, v in enumerate(labels(g)):
        order[v] = i
    offset = 0.075
    for v in g.nodes():
        pos[v] = map(add, pos[v], (offset, offset))
    nx.draw_networkx_labels(g, ax=ax, pos=pos, font_color='b',
                            labels={v: o for v, o in enumerate(order)})


if __name__ == '__main__':
    fname, g = 'dfs_example1.png', nx.petersen_graph()
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))

    te = tutte_embedding(g)

    __draw(g, ax1, 'non-recursive version', te.rpos())
    __draw_labels(g, ax=ax1, labels=non_recursive_dfs, pos=te.rpos())

    __draw(g, ax2, 'recursive version', te.rpos())
    __draw_labels(g, ax=ax2, labels=recursive_dfs, pos=te.rpos())

#    plt.savefig(fname, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
