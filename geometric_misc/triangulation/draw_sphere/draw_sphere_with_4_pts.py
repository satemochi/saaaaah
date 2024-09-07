from random import random, seed
from matplotlib import pyplot as plt
import numpy as np
import sympy as sp


def get_center_radius(pts):
    x, y, z = sp.symbols('x, y, z')
    entry = [[x**2 + y**2 + z**2, x, y, z, 1]]
    for xi, yi, zi in pts:
        entry += [[xi**2 + yi**2 + zi**2, xi, yi, zi, 1]]
    A = sp.Matrix(entry)
    B = sp.Matrix(5, 5, sp.symbols('B:5:5'))

    eq = B.det().subs(zip(list(B), list(A)))
    a, b, c, d = eq.coeff(x, 2), eq.coeff(x, 1), eq.coeff(y, 1), eq.coeff(z, 1)
    e = eq.subs(zip((x, y, z), (0, 0, 0)))

    center = (float(-b / 2 / a), float(-c / 2 / a), float(-d / 2 / a))
    radius = float((1 / 4 / a**2 * (b*b + c*c + d*d) - e/a)**0.5)
    return center, radius


def draw_sphere(center, radius, ax):
    phi, theta = np.meshgrid(np.linspace(0, np.pi, 100),
                             np.linspace(0, 2 * np.pi, 100))
    x = center[0] + radius * np.sin(phi) * np.cos(theta)
    y = center[1] + radius * np.sin(phi) * np.sin(theta)
    z = center[2] + radius * np.cos(phi)
    ax.plot_surface(x, y, z, color='#ccffcc', alpha=0.6)


def draw(pts, ax):
    ax.scatter([x for x, _, _ in pts], [y for _, y, _ in pts],
               [z for _, _, z in pts], color='k', marker='o')


def get_pts():
    return [(random(), random(), random()) for i in range(4)]


if __name__ == '__main__':
    seed(0)
    pts = get_pts()
    c, r = get_center_radius(pts)

    ax = plt.gcf().add_subplot(111, projection='3d')
    ax.set_xlim(0., 1.)
    ax.set_ylim(0., 1.)
    ax.set_zlim(0., 1.)
    ax.set_box_aspect([1., 1., 1.])

    draw(pts, ax)
    draw_sphere(c, r, ax)
    # plt.savefig('draw_sphere_with_4_pts.png', bbox_inches='tight', dpi=300)
    plt.tight_layout()
    plt.show()
