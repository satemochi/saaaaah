from itertools import combinations
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import networkx as nx
import numpy as np
from pulp import LpProblem, lpSum, LpVariable, PULP_CBC_CMD
from shapely import union_all
from shapely.affinity import scale, translate
from shapely.geometry import Polygon
from visilibity import Environment, Point, Visibility_Graph, Visibility_Polygon
from visilibity import Polygon as visPolygon


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


class guards_in_art_gallery:
    def __init__(self, poly, epsilon=1.e-6):
        self.guards = self.__get_guards(poly, epsilon)

    def __get_guards(self, poly, eps):
        g, pos, env = self.__get_visibility_graph(poly, eps)
        x = {i: LpVariable(f'x_{i}', cat='Binary') for i in g}
        lp = LpProblem()
        lp += lpSum(x)
        for i in g:
            lp += x[i] + lpSum(x[j] for j in g[i]) >= 1
        PULP_CBC_CMD(msg=0).solve(lp)
        return [(pos[i], Visibility_Polygon(Point(*pos[i]), env, eps))
                for i in g if x[i].varValue > 0]

    def __get_visibility_graph(self, poly, eps):
        env = self.__const_environment(poly)
        n, vg = env.n(), Visibility_Graph(env, eps)
        g = nx.Graph((i, j) for i, j in combinations(range(n), 2) if vg(i, j))
        pos = {i: [env(i).x(), env(i).y()] for i in g}
        return g, pos, env

    def __const_environment(self, p):
        assert not p.exterior.is_ccw
        assert all(h.is_ccw for h in p.interiors)
        verts = [Point(x, y) for x, y in reversed(p.exterior.coords[:-1])]
        boundaries = [visPolygon(verts)]
        for h in p.interiors:
            verts = [Point(x, y) for x, y in reversed(h.coords[:-1])]
            boundaries.append(visPolygon(verts))
        return Environment(boundaries)


if __name__ == '__main__':
    print('optimal vertex-gurads in an art gallery')
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

    gvd = guards_in_art_gallery(Ipe)
    for p, poly in gvd.guards:
        sp = Polygon(((poly[i].x(), poly[i].y()) for i in range(poly.n())))
        plot_polygon(plt.gca(), sp, alpha=0.3, color='darkkhaki')
        plt.scatter([p[0]], [p[1]], s=10, c='r', zorder=10)

    plot_polygon(plt.gca(), Ipe, alpha=0.1, color='gray')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()

#    plt.savefig('art_gallery_problem_in_shape_of_ipe.ipe', format='ipe')
#    plt.savefig('art_gallery_problem_in_shape_of_ipe.png',
#                bbox_inches='tight', dpi=1200)
    plt.show()
