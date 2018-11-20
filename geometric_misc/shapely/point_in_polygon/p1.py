# -*- coding: utf-8 -*-
from os.path import expanduser
import random
from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from shapely.geometry import Polygon, Point


def get_path(c, fname='/Library/Fonts/AppleGothic.ttf'):
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


def signed_area(P):
    n, area = len(P), 0
    for i in xrange(n):
        area += P[i][0] * P[(i+1) % n][1] - P[(i+1) % n][0] * P[i][1]
    return area


def is_hole(P):
    return signed_area(P) > 0


def get_polygon(c):
    path = get_path(c)
    ext, holes = None, []
    for p in path.to_polygons():
        if is_hole(p):
            holes.append(p)
        else:
            ext = p
    return Polygon(ext, holes)


def get_points(polygon, n=5000):
    xmin, ymin, xmax, ymax = polygon.bounds
    X, Y = [], []
    for i in xrange(n):
        x, y = random.uniform(xmin, xmax), random.uniform(ymin, ymax)
        if polygon.contains(Point(x, y)):
            X.append(x)
            Y.append(y)
    return X, Y


def draw_points(X, Y):
    plt.scatter(X, Y, s=1)
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    plt.savefig('contains_test_in_shapely_polygon.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    polygon = get_polygon(u'あ')
    draw_points(*get_points(polygon))
