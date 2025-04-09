from itertools import chain, combinations
from random import uniform
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import networkx as nx
import numpy as np
from rdp import rdp
from scipy.spatial.distance import euclidean
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
        p = rdp(p, 3)
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


class Triangle:
    """
        This code refer to 'circpacker: Circle Packer by author aarizat.
            (url) https://github.com/aarizat/circpacker/tree/master
        So, this code is laicensed as BSD-2-Clause license.
    """
    def __init__(self, coordinates):
        self.vertices = dict(zip('ABC', coordinates))
        self.getGeomProperties()

    def getGeomProperties(self):
        vertsArray = np.array([*self.vertices.values()])
        v = np.vstack((vertsArray, vertsArray[0]))
        # Area (Gauss Equation)
        area = 0.5*abs(sum(v[:-1, 0] * v[1:, 1] - v[:-1, 1] * v[1:, 0]))
        # length three sides triangle.
        sides = {'a': euclidean(self.vertices['B'], self.vertices['C']),
                 'b': euclidean(self.vertices['A'], self.vertices['C']),
                 'c': euclidean(self.vertices['A'], self.vertices['B'])}
        perimeter = sides['a'] + sides['b'] + sides['c']
        # Inscribed circle radius
        radius = 2*area / perimeter
        # Inscribed circle center
        center = (sides['a'] * self.vertices['A'] +
                  sides['b'] * self.vertices['B'] +
                  sides['c'] * self.vertices['C']) / perimeter
        # Distances of each vertice to incenter
        distToIncenter = [euclidean(center, v) for v in self.vertices.values()]
        setattr(self, 'distToIncenter', distToIncenter)
        setattr(self, 'incircle', Circle(center, radius))

    def circInTriangle(self, depth=None, lenght=None):
        lstCirc = [self.incircle]
        for vert, distance in zip(self.vertices.values(), self.distToIncenter):
            auxCirc = self.incircle
            auxDist = distance
            if depth is None and lenght:
                while True:
                    radius = (auxCirc.radius*auxDist -
                              auxCirc.radius**2) / (auxCirc.radius+auxDist)
                    # Checking condition stop
                    # (circle with center on the bisectrix)
                    if 2*radius <= lenght:
                        break
                    dist = auxCirc.radius + radius  # dist between centers
                    center = np.array(auxCirc.center) + (dist/auxDist) * (
                            np.array(vert) - np.array(auxCirc.center))
                    circle = Circle(center, radius)
                    # Genereting circles within triangle (Descartes circles)
                    c31, c32 = auxCirc.descartesTheorem(circle)
                    lstCirc.extend((circle, c31, c32))
                    # Updating variables
                    auxDist = euclidean(vert, circle.center)
                    auxCirc = circle
            elif lenght is None and depth >= 0:
                for i in range(1, depth+1):
                    radius = (auxCirc.radius*auxDist -
                              auxCirc.radius**2) / (auxCirc.radius+auxDist)
                    dist = auxCirc.radius + radius  # dist between centers
                    center = np.array(auxCirc.center) + (dist/auxDist) * (
                            np.array(vert) - np.array(auxCirc.center))
                    circle = Circle(center, radius)
                    # Genereting circles within triangle (Descartes circles)
                    c31, c32 = auxCirc.descartesTheorem(circle)
                    c41, c42 = auxCirc.descartesTheorem(circle, c31)
                    c51, c52 = circle.descartesTheorem(c31)
                    c61, c62 = circle.descartesTheorem(c32)
                    c71, c72 = auxCirc.descartesTheorem(c31)
                    c81, c82 = auxCirc.descartesTheorem(c32)
                    lstCirc.extend((circle, c31, c32, c41, c42, c52, c61, c71,
                                    c82))
                    # Updating variables
                    auxDist = euclidean(vert, circle.center)
                    auxCirc = circle
        return lstCirc


class Circle:
    """
        This code also refer to 'circpacker: Circle Packer by author aarizat.
            (url) https://github.com/aarizat/circpacker/tree/master
        So, this code is laicensed as BSD-2-Clause license.
    """
    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius
        self.curvature = 1 / radius
        self.diameter = 2 * radius
        self.area = np.pi * radius**2
        self.perimeter = 2 * radius * np.pi

    def descartesTheorem(self, circle1, circle2=None):

        if circle2 is None:
            # Special case Descartes' theorem
            radius = (self.curvature + circle1.curvature +
                      2*(self.curvature*circle1.curvature)**0.5)**-1
        else:
            # General case Descartes Theorem
            radius = (self.curvature + circle1.curvature +
                      circle2.radius + circle2.curvature +
                      2*((self.curvature*circle1.curvature) +
                         (circle1.curvature*circle2.curvature) +
                         (circle2.curvature*self.curvature))**0.5)**-1
        # Distances between centers and intersection points
        R1, R2 = self.radius + radius, circle1.radius + radius
        # Distance between the centers of the intersected circles
        dist = self.radius + circle1.radius
        cos, sin = (circle1.center - self.center) / dist
        # Distance to the chord
        chordDist = (R1**2 - R2**2 + dist**2) / (2*dist)
        # Half-length of the chord
        halfChord = (R1**2 - chordDist**2)**0.5
        center3 = (self.center[0] + chordDist*cos - halfChord*sin,
                   self.center[1] + chordDist*sin + halfChord*cos)
        center4 = (self.center[0] + chordDist*cos + halfChord*sin,
                   self.center[1] + chordDist*sin - halfChord*cos)
        circles = Circle(center3, radius), Circle(center4, radius)
        return circles


if __name__ == '__main__':
    print('circle packing based on Descartes theorem in triangulated Polygon')
    _I = get_polygon('I')
    assert _I.is_valid
    _p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    assert _p.is_valid
    _e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)
    assert _e.is_valid

    Ipe = union_all([_I, _p, _e])
    assert Ipe.is_valid

#    import matplotlib
#    matplotlib.use('module://backend_ipe')

    t = triangulate(get_poly_dict(Ipe), 'pq30')
    for ti in t['triangles']:
        for c in Triangle(t['vertices'][ti]).circInTriangle(lenght=7):
            cp = plt.Circle(c.center, c.radius, zorder=10,                                                  facecolor='mistyrose', lw=0.2, ec='k')
            plt.gca().add_patch(cp)
#    g = nx.Graph(chain(*(combinations(ti, 2) for ti in t['triangles'])))
#    pos = {v: t['vertices'][v] for v in g}
#    nx.draw_networkx_edges(g, pos, alpha=0.5)

    plot_polygon(plt.gca(), Ipe, alpha=0.3, color='darkgreen', ec='k')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
#    plt.savefig('circle_packing_with_descartes_theorem_in_Ipe.ipe',
#                format='ipe')
#    plt.savefig('circle_packing_with_descartes_theorem_in_Ipe.png',
#                bbox_inches='tight', dpi=900)
    plt.show()
