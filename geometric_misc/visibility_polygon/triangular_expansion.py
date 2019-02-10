# -*- coding: utf-8 -*-
import itertools
from os.path import expanduser
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.path import Path
import networkx as nx
import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import cascaded_union
import triangle


class visibility_polygon:
    """ !!!caution!!! This procedure is incomplete. Many bugs are included.

        This class visibility_polygon attempts to compute visibility polygons
        or isovists from given queries.
        Espescially, the environment is defined by a character like as 'あ'.

        We try to implement algorithm 'Triangular Expansion' refered as
        following paper;
            F. Bungiu, M. Hemmer, J. Hershberger, K. Huang, A. Kroller.
            Efficient Computation of Visiblity Polygons, EuroCG, (2014)
    """
    def __init__(self, c):
        self.path = self.__get_path(c)          # matplotlib.Path
        self.t = self.__get_triangles()         # dict with .poly format
        self.g = self.__get_nxgraph()           # networkx
        self.tgraph = self.__get_triangle_graph()
        self._sides = self.__get_sides()

    def __get_path(self, c, fname=expanduser('~/Library/Fonts/keifont.ttf')):
        """ This function is presented originally in freetype-py GitHub
            repository: we can refer the source 'glyph-vector.py' in
            the examples directory.
        """
        face = Face(fname)
        face.set_char_size(24 * 64)
        face.load_char(c)
        slot = face.glyph
        outline = slot.outline

        start, end = 0, 0
        VERTS, CODES = [], []
        for i in xrange(len(outline.contours)):
            end = outline.contours[i]
            points = outline.points[start:end+1]
            points.append(points[0])
            tags = outline.tags[start:end+1]
            tags.append(tags[0])

            segments = [[points[0], ], ]
            for j in range(1, len(points)):
                segments[-1].append(points[j])
                if tags[j] & (1 << 0) and j < (len(points)-1):
                    segments.append([points[j], ])
            verts = [points[0], ]
            codes = [Path.MOVETO, ]
            for segment in segments:
                if len(segment) == 2:
                    verts.extend(segment[1:])
                    codes.extend([Path.LINETO])
                elif len(segment) == 3:
                    verts.extend(segment[1:])
                    codes.extend([Path.CURVE3, Path.CURVE3])
                else:
                    verts.append(segment[1])
                    codes.append(Path.CURVE3)
                    for i in range(1, len(segment)-2):
                        A, B = segment[i], segment[i+1]
                        C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                        verts.extend([C, B])
                        codes.extend([Path.CURVE3, Path.CURVE3])
                    verts.append(segment[-1])
                    codes.append(Path.CURVE3)
            VERTS.extend(verts)
            CODES.extend(codes)
            start = end+1
        return Path(VERTS, CODES)

    def __get_triangles(self):
        return triangle.triangulate(self.__get_poly_dict(), 'pD')

    def __get_poly_dict(self):
        start = 0
        pslg_dict = {'vertices': [], 'holes': [], 'segments': []}
        for _p in self.path.to_polygons():
            pslg_dict['vertices'] += _p.tolist()[:-1]
            pslg_dict['segments'] += self.__get_outline_cycle(start, len(_p)-1)
            if self.__is_hole(_p):
                pslg_dict['holes'].append(self.__get_inner_point(_p[:-1]))
            start += len(_p) - 1
        if len(pslg_dict['holes']) == 0:
            del pslg_dict['holes']
        return pslg_dict

    def __get_outline_cycle(self, start, n):
        return [[start+i, start+(i+1) % n] for i in xrange(n)]

    def __is_hole(self, vertices):
        return self.__signed_area(vertices) > 0

    def __signed_area(self, P):
        n, area = len(P), 0
        for i in xrange(n):
            area += P[i][0] * P[(i+1) % n][1] - P[(i+1) % n][0] * P[i][1]
        return area

    def __get_inner_point(self, P):
        n = len(P) - 1
        return (sum(x for x, _ in P[:-1])/n, sum(y for _, y in P[:-1])/n)

    def __get_nxgraph(self):
        g = nx.Graph()
        for p, q, r in self.t['triangles']:
            pc = np.array(self.t['vertices'][p])
            qc = np.array(self.t['vertices'][q])
            rc = np.array(self.t['vertices'][r])
            g.add_edge(p, q)
            g.add_edge(q, r)
            g.add_edge(r, p)
        return g

    def __get_triangle_graph(self):
        tg = nx.Graph()
        for t1, t2 in itertools.combinations(self.t['triangles'], 2):
            if len(set(t1) & set(t2)) > 1:
                tg.add_edge(tuple(t1), tuple(t2))
        return tg

    def __get_sides(self):
        return [set(s) for s in self.t['segments']]

    def get_visibility_polygon(self, q):
        t = self.__find_triangle(q)
        if t is None:
            return
        pieces = [Polygon([self.t['vertices'][v] for v in t])]
        for i, j in enumerate(xrange(1, 4)):
            if not self.__is_side((t[i], t[j % 3])):
                tsucc, v = self.__get_diagonal_vertex(t, (t[i], t[j % 3]))
                # Triangle qrl is cut out while being star-shaped.
                a, b = self.__align_orientation(q, t[i], t[j % 3])
                r, l = self.__extend_direct(q, a), self.__extend_direct(q, b)
                assert(self.__outer_product(q, r, l) > 0)
                pieces += self.__rec_vp(q, tsucc, (a, b, v), r, l)
        return cascaded_union(pieces)

    def __find_triangle(self, p):
        for t in self.t['triangles']:
            if self.__in_triangle(p, [self.t['vertices'][i] for i in t]):
                return tuple(t)

    def __in_triangle(self, p, (p1, p2, p3)):
        a = self.__outer_product(p, p1, p2)
        b = self.__outer_product(p, p2, p3)
        c = self.__outer_product(p, p3, p1)
        return (((a > 0) and (b > 0) and (c > 0)) or
                ((a < 0) and (b < 0) and (c < 0)))

    def __outer_product(self, p1, p2, p3):
        return ((p2[0] - p1[0]) * (p3[1] - p1[1]) -
                (p3[0] - p1[0]) * (p2[1] - p1[1]))

    def __is_side(self, e):
        return set(e) in self._sides

    def __align_orientation(self, q, u, v):
        pu, pv = self.t['vertices'][u], self.t['vertices'][v]
        return (u, v) if self.__outer_product(q, pu, pv) > 0 else (v, u)

    def __get_diagonal_vertex(self, t, e):
        assert(t in self.tgraph)
        assert(not self.__is_side(e))
        se = set(e)
        for node in self.tgraph.neighbors(t):
            if se <= set(node):
                return (node, (set(node) - se).pop())

    def __extend_direct(self, q, v):
        mag = 1e1
        nq, nv = np.array(q), np.array(self.t['vertices'][v])
        return nq + mag * (nv-nq)

    def __rec_vp(self, q, t, (a, b, v), r, l):
        assert(not self.__is_side((a, b)))
        assert(self.__outer_product(q, r, l) >= 0)
        pv = self.t['vertices'][v]
        if self.__outer_product(q, r, pv) < 0:   # v is invisible from q
            return self.__get_pieces(q, t, (v, b), r, l)
        elif self.__outer_product(q, l, pv) > 0:   # Again, v is invisible
            return self.__get_pieces(q, t, (a, v), r, l)
        else:   # v is visible, then subdivide [r, l] with [r, i], [i, l]
            piece = []
            i = self.__extend_direct(q, v)
            piece += self.__get_pieces(q, t, (a, v), r, i)
            piece += self.__get_pieces(q, t, (v, b), i, l)
            return piece

    def __get_pieces(self, q, t, (a, b), r, l):
        if self.__is_side((a, b)):
            return self.__triang_with_side(q, (a, b), r, l)
        else:
            tt, vv = self.__get_diagonal_vertex(t, (a, b))
            return self.__rec_vp(q, tt, (a, b, vv), r, l)

    def __triang_with_side(self, q, (a, b), r, l):
        tv = self.t['vertices']
        s = LineString([tv[a], tv[b]])
        ir = s.intersection(LineString([q, r]))
        if ir.is_empty:
            ir = Point(tv[a])
        il = s.intersection(LineString([q, l]))
        if il.is_empty:
            il = Point(tv[b])
        return [Polygon([q] + list(ir.coords) + list(il.coords))]

    def draw_nxgraph(self):
        glyph = patches.PathPatch(self.path, facecolor='#ffcc00',
                                  alpha=0.3, lw=0, zorder=-10)
        plt.gca().add_patch(glyph)
        pos = {v: self.t['vertices'][v] for v in self.g.nodes()}
        nx.draw(self.g, pos, node_size=10, alpha=0.3)
        plt.gca().set_aspect('equal')
        plt.axis('off')


vp = visibility_polygon(u'際')

def onclick(event):
    if event.inaxes is None:
        return
    plt.cla()
    x, y = event.xdata, event.ydata
    plt.scatter([x], [y], zorder=10, s=10, edgecolor='b')

    poly = vp.get_visibility_polygon((x, y))
    if poly is not None and poly.type == 'Polygon':
        xs, ys = poly.exterior.xy
        plt.fill(xs, ys, 'g', alpha=0.5)
    vp.draw_nxgraph()
    plt.gca().set_aspect('equal')
    plt.draw()

if __name__ == '__main__':
    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    vp.draw_nxgraph()
    plt.tight_layout()
    plt.show()
