# -*- coding: utf-8 -*-
import sys
from freetype import Face
from matplotlib import cm
from matplotlib.path import Path
import networkx as nx
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
from shapely.geometry import Polygon, Point
import triangle


class gvd:
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


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    v = gvd(u'め')
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
        img.save('geo_vor.png')
        print 'saved'


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow('geodesic Voronoi diagrams')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(5.)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()
