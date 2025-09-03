from collections import deque
from functools import reduce
import math
import sys
from matplotlib import pyplot as plt, use


""" Triangulation for a simple polygon, basend ear-clipping algorithm.
    This code is licenced MIT licence, since we referenced `tripy`.
                        https://github.com/linuxlewis/tripy/tree/master
    So, we thank to @linuxlewis.

    Implementation Reference:
        - TriangulationByEarClipping.pdf
        (https://www.geometrictools.com/Documentation/Documentation.html) """

# use('module://backend_ipe')
__EPSILON = math.sqrt(sys.float_info.epsilon)


def earclip(polygon):
    if _is_clockwise(polygon):
        polygon.reverse()

    ear, triangles, n = deque(), [], len(polygon)
    prev, succ = {i: i-1 for i in range(n)}, {i: (i+1) % n for i in range(n)}
    for i in prev.keys():
        if _is_ear(prev[i], i, succ[i], polygon, prev):
            ear.append(i)

    while len(triangles) < n-2:
        i = ear.popleft()
        j, k = prev[i], succ[i]
        triangles.append((polygon[j], polygon[i], polygon[k]))
        succ[j], prev[k] = k, j
        del prev[i]
        del succ[i]
        if len(prev) > 3:
            if _is_ear(prev[j], j, succ[j], polygon, prev) and j not in ear:
                ear.append(j)
            if _is_ear(prev[k], k, succ[k], polygon, prev) and k not in ear:
                ear.append(k)
    return triangles


def _is_clockwise(polygon):
    n, _ = len(polygon), polygon
    return reduce(lambda s, i: s+(_[i+1][0]-_[i][0])*(_[i+1][1]+_[i][1]),
                  range(-1, n-1), 0) > 0


def _is_ear(i, j, k, pts, prev):
    if not _is_convex(pts[i], pts[j], pts[k]):  # diagonal pass outside ?
        return False
    if abs(_signed_area(pts[i][0], pts[i][1],   # triple collinear ?
                        pts[j][0], pts[j][1],
                        pts[k][0], pts[k][1])) < __EPSILON:
        return False
    for x in prev.keys():                       # contains no points ?
        if x in (i, j, k):
            continue
        if _is_inside(pts[x], pts[i], pts[j], pts[k]):
            return False
    return True


def _is_convex(p, q, r):
    (px, py), (qx, qy), (rx, ry) = p, q, r
    return _signed_area(px, py, qx, qy, rx, ry) < 0


def _signed_area(x1, y1, x2, y2, x3, y3):
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)


def _is_inside(p, a, b, c):
    (px, py), (ax, ay), (bx, by), (cx, cy) = p, a, b, c
    area = abs(_signed_area(ax, ay, bx, by, cx, cy))
    area1 = abs(_signed_area(px, py, bx, by, cx, cy))
    area2 = abs(_signed_area(px, py, ax, ay, cx, cy))
    area3 = abs(_signed_area(px, py, ax, ay, bx, by))
    return abs(area - sum([area1, area2, area3])) < __EPSILON


if __name__ == '__main__':
    # polygon = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    # polygon = [(-10.0, -20.0), (-10.0, -30.0), (0.0, -20.0), (0.0, -10.0),
    #            (-20.0, -10.0), (-20.0, -20.0)]
    polygon = [(350, 75), (379, 161), (469, 161), (397, 215), (423, 301),
               (350, 250), (277, 301), (303, 215), (231, 161), (321, 161)]
    plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))
    triangles = earclip(polygon)
    for t in triangles:
        plt.gca().add_patch(plt.Polygon(t, fill=False))
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.autoscale()
    plt.tight_layout()
#    plt.savefig('ear.ipe')
#    plt.savefig('ear.png', bbox_inches='tight')
    plt.show()
