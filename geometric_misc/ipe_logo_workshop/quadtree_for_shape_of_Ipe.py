from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import numpy as np
from shapely.geometry import Polygon
from shapely import union_all
from shapely.affinity import scale, translate
from quadtree import quadtree


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


if __name__ == '__main__':
    print('space decomposition with quad-tree for polygon-vertices')
    I = get_polygon('I')
    p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)

#    import matplotlib
#    matplotlib.use('module://backend_ipe')

    Ipe = union_all([I, p, e])
    xmin, ymin, _, __ = Ipe.bounds
    Ipe = translate(Ipe, xoff=-xmin, yoff=-ymin)
    s = (1 << 20) / max(Ipe.bounds)
    Ipe = scale(Ipe, s, s)
    Ipe = translate(Ipe, xoff=-Ipe.bounds[0], yoff=-Ipe.bounds[1])
    pts = np.concatenate((np.asarray(Ipe.exterior.coords),
                          *(np.asarray(h.coords) for h in Ipe.interiors)))
    qt = quadtree(pts)
    qt.qt.plot()
    plot_polygon(plt.gca(), Ipe, alpha=0.2, color='gray')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
#    plt.savefig('quadtree_for_shape_of_Ipe.ipe', format='ipe')
#    plt.savefig('quadtree_for_shape_of_Ipe.png', bbox_inches='tight', dpi=900)
    plt.show()
