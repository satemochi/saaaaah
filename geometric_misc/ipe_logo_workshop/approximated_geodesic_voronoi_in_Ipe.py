from itertools import chain, combinations, groupby
import cv2
from freetype import Face
import glfw
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import networkx as nx
import numpy as np
from numpy.linalg import norm
from OpenGL.GL import *
from rdp import rdp
from shapely import union_all
from shapely.affinity import scale, translate
from shapely.geometry import Point, Polygon
import visilibity as vis


def get_path(c, fname='Alice-Regular.ttf'):
    """ This function is presented originally of freetype-py:
        we can refer the source 'glyph-vector.py' in the examples directory.
    """
    face = Face(fname)
    face.set_char_size(24 * 64)
    face.load_char(c)
    slot = face.glyph
    outline = slot.outline

    start, end = 0, 0
    VERTS, CODES = [], []
    for i in range(len(outline.contours)):
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


def get_polygon(c):
    path = get_path(c)
    ext, holes = None, []
    for p in path.to_polygons():
        n = len(p)
        if sum(p[i][0] * p[(i+1) % n][1] - p[(i+1) % n][0] * p[i][1]
               for i in range(n)) > 0:  # if hold this then p is hole.
            holes.append(p)
        else:
            ext = p
    return Polygon(ext, holes)


def plot_polygon(ax, poly, **kwargs):
    path = Path.make_compound_path(
        Path(np.asarray(poly.exterior.coords)[:, :2]),
        *[Path(np.asarray(ring.coords)[:, :2]) for ring in poly.interiors])

    patch = PathPatch(path, **kwargs)
    collection = PatchCollection([patch], **kwargs)

    ax.add_collection(collection, autolim=True)
    ax.autoscale_view()
    return collection


class geodesic_voronoi_diagram:
    def __init__(self, poly, sites, cmap, w, h, epsilon=1.e-6):
        self.poly, self.sites, self.cmap, self.eps = poly, sites, cmap, epsilon
        self.w, self.h = w, h
        self.vg, self.env = self.__get_visibility_graph(poly)
        self.__comp_bases()

    def __get_visibility_graph(self, poly):
        env, rv = self.__const_environment(poly)
        vg = vis.Visibility_Graph(env, self.eps)
        nx_vg = nx.Graph()
        for ui, vi in combinations((i for i in range(vg.n())
                                    if [env(i).x(), env(i).y()] in rv), 2):
            if vg(ui, vi):
                dist = norm(np.array((u := (env(ui).x(), env(ui).y()))) -
                            np.array((v := (env(vi).x(), env(vi).y()))))
                nx_vg.add_edge(u, v, weight=dist)
        return nx_vg, env

    def __const_environment(self, p, delta=1.0):
        assert not p.exterior.is_ccw
        assert all(h.is_ccw for h in p.interiors)
        simp = rdp(list(reversed(p.exterior.coords[:-1])), delta)
        boundaries = [vis.Polygon([vis.Point(x, y) for x, y in simp])]
        reflex = [simp[i] for i in range(-1, len(simp)-1)
                  if not self.__ccw(simp[i-1], simp[i], simp[i+1])]
        for h in p.interiors:
            simp = rdp(list(reversed(h.coords[:-1])), delta)
            boundaries.append(vis.Polygon([vis.Point(x, y) for x, y in simp]))
            reflex += [simp[i] for i in range(-1, len(simp)-1)
                       if not self.__ccw(simp[i-1], simp[i], simp[i+1])]
        return vis.Environment(boundaries), reflex

    @staticmethod
    def __ccw(p, q, r):
        (px, py), (qx, qy), (rx, ry) = p, q, r
        return ((qx - px) * (ry - py) - (qy - py) * (rx - px)) > 0

    def __comp_bases(self):
        for v in self.vg:
            self.vg.nodes[v]['base'] = self.__get_base_coordinates(v)

    def __get_base_coordinates(self, s):
        cpts, o = self.__get_circum_points(s), np.array(s)
        return [(p[0], p[1], norm(o - np.array(p))) for p in cpts]

    def __get_circum_points(self, p, minlen=10):
        vertices = self.__get_snapped_vertices(self.__get_isovist(p))
        n, o, points = len(vertices), np.array(p), []
        for i in range(n):
            _p, _q = np.array(vertices[i]), np.array(vertices[(i+1) % n])
            if all(o == _p) or all(o == _q):
                if all(o == _q):
                    points.append(p)
                continue
            dist = norm(_p - _q)
            sdiv_count = int(np.ceil(dist / minlen))
            pts = zip(np.linspace(_p[0], _q[0], sdiv_count),
                      np.linspace(_p[1], _q[1], sdiv_count))
            points += pts
        return (a := [p[0] for p in groupby(points)]) + [a[0]]

    def __get_isovist(self, p):
        v = vis.Point(*p)
        v.snap_to_boundary_of(self.env, self.eps)
        v.snap_to_vertices_of(self.env, self.eps)
        return vis.Visibility_Polygon(v, self.env, self.eps)

    def __get_snapped_vertices(self, isovist):
        vertices = []
        for i in range(isovist.n()):
            p = isovist[i]
            p.snap_to_vertices_of(self.env, self.eps)
            p.snap_to_boundary_of(self.env, self.eps)
            vertices.append((p.x(), p.y()))
        return vertices + [vertices[0]]

    def draw(self):
        for s, c in zip(self.sites, self.cmap):
            glColor3ubv(c)
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
            for p in self.vg.nodes[v]['base']:
                glVertex3f(*p)
            glEnd()
            glPopMatrix()

    def __geodesic_distances(self, s):
        vertices = self.__get_snapped_vertices(self.__get_isovist(s))
        _s = np.array(s)
        for v in vertices:
            if v in self.vg:
                self.vg.add_edge(v, s, weight=norm(np.array(v) - _s))
        lengths = nx.single_source_dijkstra_path_length(self.vg, s)
        self.vg.remove_node(s)
        return lengths

    def get_boundaries(self):
        self.draw()
        buf = glReadPixels(0, 0, self.w, self.h, GL_RED, GL_UNSIGNED_BYTE)
        image = np.frombuffer(buf, dtype=np.uint8).reshape(self.h, self.w)
        cv2.imwrite("red_pattern.png", image[::-1])

        for s, c in zip(self.sites, self.cmap):
            yield self.__boundary_tracing(s, c, image)

    def __boundary_tracing(self, s, c, img):
        x, y = s
        x1, y1, x2, y2 = self.poly.bounds
        aw, ah = x2 - x1, y2 - y1

        gx = int(self.w * (x - x1) / aw)
        gy = int(self.h * (y - y1) / ah)
        assert img[gy][gx] == c[0]

        boundaries, d = [self.__find_left_most(img, c, gx, gy)], 4
        while True:
            d = (d + 6) & 7 if d & 1 else (d + 7) & 7
            while True:
                next_x, next_y = boundaries[-1]
                if d == 0:
                    next_y += 1
                elif d == 1:
                    next_x, next_y = next_x - 1, next_y + 1
                elif d == 2:
                    next_x -= 1
                elif d == 3:
                    next_x, next_y = next_x - 1, next_y - 1
                elif d == 4:
                    next_y -= 1
                elif d == 5:
                    next_x, next_y = next_x + 1, next_y - 1
                elif d == 6:
                    next_x += 1
                elif d == 7:
                    next_x, next_y = next_x + 1, next_y + 1
                if self.__check_valid_image_boundaries(img, c, next_x, next_y):
                    boundaries.append((next_x, next_y))
                    break
                d = (d + 1) & 7
            if len(boundaries) >= 4:
                if (boundaries[-1] == boundaries[1] and
                        boundaries[-2] == boundaries[0]):
                    break

        return [(gx * aw / self.w + x1, gy * ah / self.h + y1)
                for gx, gy in boundaries]

    def __find_left_most(self, img, c, gx, gy):
        for x in range(gx, -1, -1):
            if img[gy][x] != c[0]:
                return (x+1, gy)
        return (0, gy)

    def __check_valid_image_boundaries(self, img, c, next_x, next_y):
        if (next_y >= self.h or next_x < 0 or next_y < 0 or next_x >= self.w):
            return False
        if img[next_y][next_x] == c[0]:
            return True


def setup(w, h, poly):
    x1, y1, x2, y2 = poly.bounds
    glViewport(0, 0, w, h)
    glOrtho(x1, x2, y1, y2, (_ := max(x2-x1, y2-y1)), -_)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def save(w, h):
    image_buffer = glReadPixels(0, 0, w, h, GL_BGR, GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(h, w, 3)[::-1]
    cv2.imwrite("aproximated_geodesic_voronoi_drawing_in_Ipe.png", image)


if __name__ == '__main__':
    print('approximated geodesic Voronoi diagram in a polygon with holes')
    _I = get_polygon('I')
    assert _I.is_valid
    assert not _I.exterior.is_ccw
    _p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    assert _p.is_valid
    _e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)
    assert _e.is_valid

#    import matplotlib
#    matplotlib.use('module://backend_ipe')

    Ipe = union_all([_I, _p, _e])
    assert Ipe.is_valid
    sites = [(120, 50), (1290, 400), (350, 322), (1150, 0), (750, 420)]
    cmap = [(153, 0, 0), (175, 97, 16), (191, 144, 0), (56, 118, 29),
            (19, 79, 92)]

    x1, y1, x2, y2 = Ipe.bounds
    w, h = 1200, int(1200 * (y2 - y1) / (x2 - x1))
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, False)
    window = glfw.create_window(w, h, "hidden window", None, None)
    glfw.make_context_current(window)
    setup(w, h, Ipe)

    gvd = geodesic_voronoi_diagram(Ipe, sites, cmap, w, h)
    for i, b in enumerate(gvd.get_boundaries()):
        sb = rdp(b, 0.5)
        c = ('#' + hex(cmap[i][0])[2:].zfill(2) + hex(cmap[i][1])[2:].zfill(2)
             + hex(cmap[i][2])[2:].zfill(2))
        plt.gca().add_patch(plt.Polygon(sb, fc=c))

    save(w, h)
    glfw.destroy_window(window)
    glfw.terminate()

    plot_polygon(plt.gca(), Ipe, alpha=0.2, color='w')
    plt.scatter([x for x, _ in sites], [y for _, y in sites], s=5, c='k')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()

#    plt.savefig('approximated_geodesic_voronoi_in_Ipe.ipe', format='ipe')
#    plt.savefig('approximated_geodesic_voronoi_in_Ipe.png',
#                bbox_inches='tight')
    plt.show()
