from matplotlib import pyplot as plt, use
from sympy import diff, I, im, latex, nroots, re, Point
from sympy.abc import x
from sympy.geometry.util import convex_hull


def draw_convex_hull(roots):
    hull = convex_hull(*[Point(r.as_real_imag()) for r in roots])
    _x = [float(p.x) for p in hull.vertices]
    _y = [float(p.y) for p in hull.vertices]
    plt.plot(_x + [_x[0]], _y + [_y[0]])
    plt.scatter([re(_) for _ in roots], [im(_) for _ in roots])


if __name__ == '__main__':
    """ A snippet for Gauss-Lucas theorem """
    # expr = x**6 + 3*I*x**5 - 2*x**4 + 9*x**3 - 4*x**2 + x - 1
    expr = x**8 -1/5*I*x**7 +1/4*x**6 +3*I*x**5 -2*x**4 +9*x**3 -4*x**2 +x -1
    # expr = x**5 - 3*x**3 - x**2 - x + 1
    print(latex(expr))
    roots, d_roots = nroots(expr), nroots(diff(expr, x))

    # use('module://backend_ipe')
    draw_convex_hull(roots)
    draw_convex_hull(d_roots)

    plt.gca().set_title('$' + str(latex(expr)) + ' = 0$')
    plt.gca().grid()
    plt.gca().autoscale()
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    # plt.savefig('gaus_lucas.ipe')
    plt.show()
