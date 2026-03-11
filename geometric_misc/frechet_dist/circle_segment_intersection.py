from math import isclose, sqrt
from matplotlib import pyplot as plt



def circle_line_segment_intersection(c, r, pt1, pt2):
    """ Find the points at which a circle intersects a line-segment.
        This can happen at 0, 1, or 2 points.
            http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, c
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr, d = dx * dx + dy * dy, x1 * y2 - x2 * y1
    if (discriminant := (r * r) * dr  - (d * d)) < 0:
        return []
    sqrt_d = sqrt(discriminant)

    i = [(cx + (d * dy + sign * (-1 if dy < 0 else 1) * dx * sqrt_d) / dr,
          cy + (-d * dx + sign * abs(dy) * sqrt_d) / dr )
         for sign in ((1, -1) if dy < 0 else (-1, 1))]

    frac = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy
            for xi, yi in i]

    if len(frac) == 2:
        if frac[0] > 1 or frac[1] < 0:
            return False
        if not isclose(discriminant, 0):
            return [max(frac[0], 0), min(frac[1], 1)]
        frac = [frac[0]]
    if 0 <= frac[0] <= 1:
        return frac
    return []


def lerp(p, q, t):
    """ linear interpolation: return new point: (1 - t)a + tb """
    (x, y), (_x, _y) = p, q
    return ((_t := 1 - t)*x + t*_x, _t*y + t*_y)


if __name__ == '__main__':
    c, r = (0.5, 0.5), 0.25
#    s0, s1 = (0.1, 0.1), (0.6, 0.45)   # crossing with one point
#    s0, s1 = (0.1, 0.1), (0.6, 0.25)    # non-crossing

    s0, s1 = (0.1, 0.7), (0.8, 0.1)     # crossing with two points
#    s0, s1 = (0.8, 0.1), (0.1, 0.7)

#    s0, s1 = (0.1, 0.75), (0.8, 0.75)   # tangent line
#    s0, s1 = (0.1, 0.75), (0.3, 0.75)   # not tangent line
#    s0, s1 = (0.1, 0.75-0.000001), (0.8, 0.75)   # non-tangent line

#    s0, s1 = (0.4, 0.4), (0.6, 0.5)   # included

#    c, r = (1.0, 0.4957732931341461), 0.4
#    s0 = (0.3333333333333333, 0.13382952895927658)
#    s1 = (0.6666666666666666, 0.14211108545453854)

    frac = circle_line_segment_intersection(c, r, s0, s1)
    print(frac)
    if frac:
        intersections = [lerp(s0, s1, t) for t in frac]
        plt.scatter([x for x, _ in intersections],
                    [y for _, y in intersections], color='r', ec='k', zorder=5)


    plt.gca().add_artist(plt.Circle(c, r, fill=False, color='g'))
    plt.scatter([c[0]], [c[1]], color='g', ec='k')

    plt.plot([s0[0], s1[0]], [s0[1], s1[1]])
    plt.scatter([s0[0], s1[0]], [s0[1], s1[1]],
                color='orange', ec='k', zorder=5)

    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 1)
    plt.tight_layout()
    plt.show()
