from itertools import chain
from math import sqrt
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection, LineCollection
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, LineString
from shapely import union_all
from shapely.affinity import scale, translate


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


class line_voro:
    def __init__(self, segs):
        self.points = list(chain.from_iterable(self.__split(s) for s in segs))
        v = Voronoi(self.points)
        self.ridges = (v.vertices[r] for r in v.ridge_vertices if -1 not in r)

    @staticmethod
    def __split(s):
        (x0, y0), (x1, y1) = s
        if (n := sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))) < 5:
            return s
        dx, dy = (x1 - x0) / n, (y1 - y0) / n
        return [(x0 + dx*i, y0 + dy*i) for i in range(int(n))]


if __name__ == '__main__':
    print('Medial axis (slitely diff) with Voronoi diagram for line segments')
    _I = get_polygon('I')
    assert _I.is_valid
    _p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    assert _p.is_valid
    _e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)
    assert _e.is_valid

    import matplotlib
    matplotlib.use('module://backend_ipe')

    Ipe = union_all([_I, _p, _e])
    assert Ipe.is_valid

    b = Ipe.exterior.coords
    segs = [b[k:k+2] for k in range(len(b) - 1)]
    for b in Ipe.interiors:
        segs += list(zip((_ := np.asarray(b.coords)), _[1:]))

    lv = line_voro(segs)
    for s in lv.ridges:
        if Ipe.covers(LineString(s)):
            plt.plot([s[0][0], s[1][0]], [s[0][1], s[1][1]], c='g', lw=0.8)

    plot_polygon(plt.gca(), Ipe, alpha=0.5, color='goldenrod')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    plt.savefig('medial_axis_with_segment_voronoi.ipe', format='ipe')
    plt.savefig('medial_axis_with_segment_voronoi.png', bbox_inches='tight',
                dpi=900)
#    plt.show()
