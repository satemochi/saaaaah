import itertools
import sys
import numpy as np
import networkx as nx
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import visilibity as vis


class geodesic_voronoi_diagram:
    def __init__(self, environment, reflex_vertices, epsilon=1.e-6):
        self.env = environment
        self.rv = reflex_vertices
        self.eps = epsilon
        self.vg = self.__get_visibility_graph()
        self.__comp_bases()

    def __get_visibility_graph(self):
        vg = vis.Visibility_Graph(self.env, self.eps)
        nx_vg = nx.Graph()
        tgt = [i for i in xrange(vg.n()) if self.__is_reflex(self.env(i))]
        for i, j in itertools.combinations(tgt, 2):
            if vg(i, j):
                u = (self.env(i).x(), self.env(i).y())
                v = (self.env(j).x(), self.env(j).y())
                dist = np.linalg.norm(np.array(u) - np.array(v))
                nx_vg.add_edge(u, v, weight=dist)
        return nx_vg

    def __is_reflex(self, vis_point):
        px, py, e = vis_point.x(), vis_point.y(), self.eps
        for x, y in self.rv:
            if (px-e < x and x < px+e) and (py-e < y and y < py+e):
                return True
        return False

    def __comp_bases(self):
        for v in self.rv:
            self.vg.node[v]['base'] = self.__get_base_coordinates(v)

    def __get_base_coordinates(self, s):
        cpts = self.__get_circum_points(s)
        o = np.array(s)
        return [(p[0], p[1], np.linalg.norm(o - np.array(p))) for p in cpts]

    def __get_circum_points(self, p, minlen=10):
        vertices = self.__get_isovist_vertices(p)
        n, o, points = len(vertices), np.array(p), []
        for i in xrange(n):
            _p, _q = np.array(vertices[i]), np.array(vertices[(i+1) % n])
            if all(o == _p) or all(o == _q) or self.__collinear(o, _p, _q):
                if all(o == _q):
                    points.append(p)
                continue
            dist = np.linalg.norm(_p - _q)
            sdiv_count = np.ceil(dist / minlen)
            pts = zip(np.linspace(_p[0], _q[0], sdiv_count),
                      np.linspace(_p[1], _q[1], sdiv_count))
            points += pts
        return [p[0] for p in itertools.groupby(points)]

    def __get_isovist_vertices(self, p):
        return self.__get_snapped_vertices(self.__get_isovist(p))

    def __get_isovist(self, p):
        v = vis.Point(*p)
        v.snap_to_boundary_of(self.env, self.eps)
        v.snap_to_vertices_of(self.env, self.eps)
        return vis.Visibility_Polygon(v, self.env, self.eps)

    def __get_snapped_vertices(self, isovist):
        vertices = []
        for i in xrange(isovist.n()):
            p = isovist[i]
            p.snap_to_vertices_of(self.env, self.eps)
            p.snap_to_boundary_of(self.env, self.eps)
            vertices.append((p.x(), p.y()))
        return vertices

    def __collinear(self, o, p, q):
        s1 = vis.Line_Segment(vis.Point(*o), vis.Point(*p))
        if vis.Point(*q).in_relative_interior_of(s1, self.eps):
            return True
        s2 = vis.Line_Segment(vis.Point(*o), vis.Point(*q))
        if vis.Point(*p).in_relative_interior_of(s2, self.eps):
            return True
        return False
    def draw(self, s):
        self.__draw_site(s)
        self.__draw_reflexes(s)

    def __draw_site(self, s):
        bases = self.__get_base_coordinates(s)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*s)
        for p in bases:
            glVertex3f(*p)
        glEnd()

    def __draw_reflexes(self, s):
        dist = self.__geodesic_distances(s)
        for v in self.vg:
            glPushMatrix()
            glTranslatef(0, 0, dist[v])
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(*v)
            for p in self.vg.node[v]['base']:
                glVertex3f(*p)
            glEnd()
            glPopMatrix()

    def __geodesic_distances(self, s):
        vertices = self.__get_isovist_vertices(s)
        _s = np.array(s)
        for v in vertices:
            if v in self.vg:
                self.vg.add_edge(v, s, weight=np.linalg.norm(np.array(v) - _s))
        lengths = nx.single_source_dijkstra_path_length(self.vg, s)
        self.vg.remove_node(s)
        return lengths

    def draw_apex(self, (x, y)):
        glColor4f(1., 1., 1., 1.)
        glBegin(GL_POINTS)
        glVertex3f(x, y, -1)
        glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    sites, obj, env, reflexes = get_instance()
    gvd = geodesic_voronoi_diagram(env, reflexes)
    np.random.seed(4)
    for s in sites:
        glColor3f(*np.random.rand(3))
        gvd.draw(s)
        gvd.draw_apex(s)
    glutSwapBuffers()


def get_instance():
    sites = [(600, 550), (300, 400), (50, 100), (800, 100), (950, 980)]
    objects, elements, corners = [], [], []
    wall = [(0, 0), (1000, 0), (1000, 1000), (0, 1000)]
    objects.append(wall)
    elements.append(vis.Polygon([vis.Point(x, y) for x, y in wall]))

    hole1 = [(100, 300), (100, 500), (150, 500), (150, 300)]
    objects.append(hole1)
    elements.append(vis.Polygon([vis.Point(x, y) for x, y in hole1]))
    corners += hole1

    hole2 = [(300, 700), (300, 800), (550, 800), (550, 700)]
    objects.append(hole2)
    elements.append(vis.Polygon([vis.Point(x, y) for x, y in hole2]))
    corners += hole2

    hole3 = [(700, 300), (700, 650), (850, 650), (850, 300)]
    objects.append(hole3)
    elements.append(vis.Polygon([vis.Point(x, y) for x, y in hole3]))
    corners += hole3

    hole4 = [(300, 100), (300, 200), (450, 200), (450, 100)]
    objects.append(hole4)
    elements.append(vis.Polygon([vis.Point(x, y) for x, y in hole4]))
    corners += hole4

    env = vis.Environment(elements)
    return sites, objects, env, corners


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000.0, 0.0, 1000.0, 1.0, -2000.0)


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

    # window settings
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("The geodesic Voronoi drawing")

    # to enable hidden surface elimination and so on
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # to enable anti-aliasing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(4)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()
