from itertools import chain, combinations
from random import uniform
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import networkx as nx
import numpy as np
from shapely.geometry import Polygon, Point
from shapely import union_all
from shapely.affinity import scale, translate
from triangle import triangulate


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


def get_poly_dict(polygon):
    pslg_dict = {}
    pslg_dict['vertices'] = list(polygon.exterior.coords[:-1])
    n = len(pslg_dict['vertices'])
    pslg_dict['segments'] = [(i, (i + 1) % n) for i in range(n)]
    if len(polygon.interiors) > 0:
        pslg_dict['holes'] = []
    for h in polygon.interiors:
        s = len(pslg_dict['vertices'])
        pslg_dict['vertices'] += (a := list(h.coords[:-1]))
        n = len(a)
        pslg_dict['segments'] += [(s + i, s + (i + 1) % n) for i in range(n)]
        pslg_dict['holes'].append((sum(x for x, _ in a) / n,
                                   sum(y for _, y in a) / n))
    return pslg_dict


if __name__ == '__main__':
    # print('constrained triangulations for a polygon with holes')
    I = get_polygon('I')
    assert I.is_valid
    p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    assert p.is_valid
    e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)
    assert e.is_valid

#    import matplotlib
#    matplotlib.use('module://backend_ipe')

    Ipe = union_all([I, p, e])
    assert Ipe.is_valid

    t = triangulate(get_poly_dict(Ipe), 'pq30')
#    t = triangulate(get_poly_dict(Ipe), 'pD')
    g = nx.Graph(chain(*(combinations(ti, 2) for ti in t['triangles'])))
    pos = {v: t['vertices'][v] for v in g}
    nx.draw_networkx_edges(g, pos, alpha=0.5)

    plot_polygon(plt.gca(), Ipe, alpha=0.2, color='yellow')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
#    plt.savefig('constrained_triangulations_with_shape_of_Ipe.ipe',
#                format='ipe')
#    plt.savefig('constrained_triangulations_with_shape_of_Ipe.png',
#                bbox_inches='tight')
    plt.show()
