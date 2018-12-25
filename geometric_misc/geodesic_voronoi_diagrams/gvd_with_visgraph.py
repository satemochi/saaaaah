# -*- coding: utf-8 -*-
import itertools
import sys
from freetype import Face
from matplotlib import cm
from matplotlib.path import Path
import networkx as nx
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
from shapely.geometry import Polygon, Point, LineString
import triangle
import visilibity as vis


class gvd:
    epsilon = 1.0e-12

    def __init__(self, c):
        self.path = self.__get_path(c)          # matplotlib.Path
        self.t = self.__get_triangles()         # dict with .poly format
        self.g = self.__get_nxgraph()           # networkx
        self.polygon = self.__get_polygon()     # shapely Polygon

    def __get_path(self, c, fname='/Library/Fonts/AppleGothic.ttf'):
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
        return triangle.triangulate(self.__get_poly_dict(), 'pqa50')

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
        n = len(P)
        return (sum(x for x, _ in P)/n, sum(y for _, y in P)/n)

    def __get_nxgraph(self):
        g = nx.Graph()
        for p, q, r in self.t['triangles']:
            pc = np.array(self.t['vertices'][p])
            qc = np.array(self.t['vertices'][q])
            rc = np.array(self.t['vertices'][r])
            g.add_edge(p, q, weight=np.linalg.norm(qc - pc))
            g.add_edge(q, r, weight=np.linalg.norm(rc - qc))
            g.add_edge(r, p, weight=np.linalg.norm(pc - rc))
        return g

    def __get_polygon(self):
        """ assuming given polygon is single component. """
        ext, holes = None, []
        for p in self.path.to_polygons():
            if self.__is_hole(p):
                holes.append(p)
            else:
                ext = p
        return Polygon(ext, holes)

    def get_instance(self, n=3, seed=9):
        np.random.seed(seed)
        xmin, ymin, xmax, ymax = self.polygon.bounds
        S = []
        while len(S) < n:
            x, y = np.random.uniform(xmin, xmax), np.random.uniform(ymin, ymax)
            if self.polygon.contains(Point(x, y)):
                S.append((x, y))
        return S

    def get_mesh(self, p):
        t = self.__find_triangle(p)
        if t is not None:
            pslg_dict = {'vertices': [],
                         'triangles': self.t['triangles'].tolist()}
            length = self.__shortest_path_length(t, p)
            for i, dist in length.items():
                x, y = self.t['vertices'][i]
                pslg_dict['vertices'].append((x, y, dist))
            self.__append_apex(pslg_dict, t, p)
            return pslg_dict

    def __append_apex(self, pslg_dict, t, (x, y)):
        v = self.g.number_of_nodes()
        pslg_dict['vertices'].append([x, y, 0])
        pslg_dict['triangles'].append([t[0], t[1], v])
        pslg_dict['triangles'].append([t[1], t[2], v])
        pslg_dict['triangles'].append([t[2], t[0], v])

    def __find_triangle(self, p):
        for t in self.t['triangles']:
            if self.__in_triangle(p, [self.t['vertices'][i] for i in t]):
                return t

    def __in_triangle(self, p, (p1, p2, p3)):
        a = self.__outer_product(p, p1, p2)
        b = self.__outer_product(p, p2, p3)
        c = self.__outer_product(p, p3, p1)
        return (((a > 0) and (b > 0) and (c > 0)) or
                ((a < 0) and (b < 0) and (c < 0)))

    def __outer_product(self, p1, p2, p3):
        return ((p2[0] - p1[0]) * (p3[1] - p1[1]) -
                (p3[0] - p1[0]) * (p2[1] - p1[1]))

    def __shortest_path_length(self, t, p):
        v = self.g.number_of_nodes()
        p = np.array(p)
        for u in t:
            uc = np.array(self.t['vertices'][u])
            self.g.add_edge(u, v, weight=np.linalg.norm(uc - p))
        length = nx.single_source_dijkstra_path_length(self.g, v)
        del length[v]
        self.g.remove_node(v)
        return length

    def get_vis_net(self, S):
        env, vg = self.__get_vis()
        nx_vg, pos = self.__get_nx_vis_graph(vg, env)
        V = []
        for s in S:
            V.append(self.__add_sites(s, nx_vg, pos, env))
        return self.__get_vlines(V, nx_vg, pos)

    def __get_vis(self):
        poly = []
        for p in self.path.to_polygons():
            poly.append(vis.Polygon([vis.Point(*v) for v in p[:-1][::-1]]))
        env = vis.Environment(poly)
        vg = vis.Visibility_Graph(env, self.epsilon)
        return env, vg

    def __get_nx_vis_graph(self, vg, env):
        nx_vg, pos = nx.Graph(), {}
        for u, v in itertools.combinations(xrange(vg.n()), 2):
            if vg(u, v):
                p, q = env(u), env(v)
                p.snap_to_vertices_of(env, self.epsilon)
                q.snap_to_vertices_of(env, self.epsilon)
                _p, _q = (p.x(), p.y()), (q.x(), q.y())
                nx_vg.add_edge(u, v, weight=self.__dist(_p, _q))
                if u not in pos:
                    pos[u] = _p
                if v not in pos:
                    pos[v] = _q
        return nx_vg, pos

    def __dist(self, p, q):
        return np.linalg.norm(np.array(p) - np.array(q))

    def __add_sites(self, s, nx_vg, pos, env):
        node = nx_vg.number_of_nodes()
        pos[node] = tuple(s)
        isovist = vis.Visibility_Polygon(vis.Point(*s), env, self.epsilon)
        for i in xrange(isovist.n()):
            p = isovist[i]
            p.snap_to_vertices_of(env, self.epsilon)
            _p = (p.x(), p.y())
            for k, v in pos.items():
                if _p == v:
                    nx_vg.add_edge(node, k, weight=self.__dist(s, _p))
        return node

    def __get_vlines(self, V, nx_vg, pos):
        L = []
        for u, v in itertools.combinations(V, 2):
            if self.__mutually_visible(u, v, pos):
                L.append((pos[u], pos[v]))
            else:
                path = nx.dijkstra_path(nx_vg, u, v)
                for i, j in zip(path[:-1], path[1:]):
                    if not self.g.has_edge(i, j):
                        L.append((pos[i], pos[j]))
        return L

    def __mutually_visible(self, u, v, pos):
        ell = LineString([pos[u], pos[v]])
        return ell.intersection(self.polygon).type == 'LineString'


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    v = gvd(u'め')
#    v = gvd(u'を')
#    v = gvd(u'あ')
    S = v.get_instance(5)
    for s in S:
        x, y = s
        glColor3f(1., 1., 1.)
        glBegin(GL_POINTS)
        glVertex3f(x, y, 0)
        glEnd()
        glColor4f(*(cm.nipy_spectral(np.sqrt(x*x + y*y) / 1500.)))
        mesh = v.get_mesh(s)
        glBegin(GL_TRIANGLES)
        for t in mesh['triangles']:
            for i in t:
                glVertex3f(*(mesh['vertices'][i]))
        glEnd()
    lines = v.get_vis_net(S)
    glColor4f(0.6, 0.6, 0.6, 0.8)
    glBegin(GL_LINES)
    for u, v in lines:
        glVertex2f(*u)
        glVertex2f(*v)
    glEnd()
    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(200., 1400., -50., 1150., 0., -1200.)


def keyboard(key, x, y):
    if key == '\033' or key == 'q':
        sys.exit()
    if key == 's':
        glReadBuffer(GL_FRONT)
        w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        buf = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
        img = Image.frombytes(mode="RGB", size=(w, h), data=buf)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save('geo_vor2_.png')
        print 'saved'


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(1000, 100)
    glutCreateWindow('geodesic Voronoi diagrams')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(5.)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(3.)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()
