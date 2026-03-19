from matplotlib import pyplot as plt
import numpy as np


def ellipse_coeffs(pts):
    A, b = [[x*x, x*y, y*y, x, y] for x, y in pts], [-1] * 5
    return np.linalg.solve(A, b)


def get_params(coeffs):
    """ ref) Ellipse#General_ellipse_2 - wikipedia.en """
    a, b, c, d, e = coeffs
    if (denom := b * b - 4 * a * c) >= 0:
        raise ValueError(f'{denom} = b^2 - 4ac >= 0')
    x = a*e*e + c*d*d - b*d*e + denom
    ya = a + c + np.sqrt((a - c)**2 + b*b)
    yb = a + c - np.sqrt((a - c)**2 + b*b)
    return (-np.sqrt(2 * x * ya) / denom,               # long axis
            -np.sqrt(2 * x * yb) / denom,               # short axis
            (2*c*d - b*e) / denom,                      # center-x
            (2*a*e - b*d) / denom,                      # center-y,
            0.5 * np.atan2(-b, c - a) * 180 / np.pi)    # angle


def gen_pts(s=9):
    from random import random, seed
    seed(s)
    pts = [(random(), random()) for i in range(3)]
    while len(pts) < 5:
        pts.append((random(), random()))
        if len(__convex_hull(pts)) != len(pts):
            pts.pop()
    return pts


def __convex_hull(pts):
    """ A gift wrapping algorithm for convex hull of 2d points """
    ch = [min(pts)]     # start from leftmost and lowest
    while True:         # try to find support lines
        q = next((targets := iter(_ for _ in pts if _ != ch[-1])))
        for r in targets:
            if __is_right_turn(ch[-1], q, r):
                q = r
        if q == ch[0]:
            break
        ch.append(q)
    return ch


def __is_right_turn(p, q, r):
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    if (c := x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)) != 0:
        return c > 0
    return ((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)       # on tie (collinear)
            < (x1-x3) * (x1-x3) + (y1-y3) * (y1-y3))    # won by far to ch[-1]


if __name__ == '__main__':
    pts = gen_pts()
    plt.scatter([x for x, _ in pts], [y for _, y in pts], ec='k', zorder=3)

    try:
        w, h, cx, cy, angle = get_params(ellipse_coeffs(pts))
        from matplotlib.patches import Ellipse
        ellipse = Ellipse(xy=(cx, cy), width=w*2, height=h*2, angle=angle,
                          ec='blue', fc='none', lw=2)
        plt.gca().add_patch(ellipse)
    except ValueError as e:
        print(f'[ellipse undefined]\n\t{e.__class__.__name__}: {e}')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    plt.show()
