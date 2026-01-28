from math import sqrt
from matplotlib import pyplot as plt
import numpy as np


"""
    Demonstrate c function line_line_closest_points3d (original mention)
        # we translated with python.

        The following is robust C code from Seth Teller that computes the
        "points of closest approach" on two 3D lines.  It also classifies
        the lines as parallel, intersecting, or (the generic case) skew.

        [ref]: https://people.csail.mit.edu/teller/geomlib/linelinecp.c
"""

eps = 1e-7
maxreciplen = 1. / eps


class point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def dist(self, other):
        (x, y, z), (_x, _y, _z) = self, other
        return sqrt(sum(di**2 for di in [x - _x, y - _y, z - _z]))

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __add__(self, other):
        """ vector sum """
        return point(*(xi + _xi for xi, _xi in zip(self, other)))

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def cross(self, other):
        """ cross/outer product with `self` times `other` """
        (x, y, z), (_x, _y, _z) = self, other
        return point(y * _z - z * _y, z * _x - x * _z, x * _y - y * _x)

    def dot(self, other):
        """ dot/inner product with `self` times `other` """
        return sum(xi * _xi for xi, _xi in zip(self, other))

    def mag(self):
        """ distance from the origin (`hypot` in python math package) """
        return sqrt(self.dot(self))

    def recip_mag(self):
        """ reciprocal (inversed) magnitude """
        return 1. / self.mag()

    def norm(self):
        """ normalize vector of self (same direction and unit norm) """
        if (d := self.recip_mag()) > maxreciplen:
            return point(0, 0, 0)
        return point(self.x * d, self.y * d, self.z * d)

    def dist_to_plane(self, f):
        """ dist from `self` to `f` """
        (x, y, z), (a, b, c, d) = self, f
        return (x * a) + (y * b) + (z * c) + d

    def lerp(self, other, t):
        """ linear interpolation: return new point: (1 - t)a + tb """
        (x, y, z), (_x, _y, _z) = self, other
        return point((_t := 1 - t)*x + t*_x, _t*y + t*_y, _t*z + t*_z)

    @classmethod
    def line_line_closest_point3d(self, adir, a, bdir, b):
        """ computes pair of points pA on line A and  pB on line B such that
            pA and pB are closest each other. """
        # connecting line is perpendicular to both
        if (cdir := adir.cross(bdir).norm()).mag() <= eps:
            # lines are near-parallel -- infinitely many pairs being closest
            return a, b
        ac = plane.from_two_vectors_and_point(cdir, adir, a)
        bc = plane.from_two_vectors_and_point(cdir, bdir, b)
        pA = bc.intersect_from_line_through(a, a + adir)
        pB = ac.intersect_from_line_through(b, b + bdir)
        return (pA, pB)

    def draw(self):
        plt.gca().scatter([self.x], [self.y], [self.z], color='k', marker='o')

    def draw_line(self, other):
        (x, y, z), (_x, _y, _z) = self, other
        plt.gca().plot([x, _x], [y, _y], [z, _z])


class plane:
    def __init__(self, a, b, c, d):
        """ plane: ax + by + cz + z = 0 """
        self.a, self.b, self.c, self.d = a, b, c, d

    def __iter__(self):
        """ to be used to unpack coordinates """
        return iter((self.a, self.b, self.c, self.d))

    def __repr__(self):
        return f"plane: {self.a}x + {self.b} y + {self.c} z + {self.d} = 0"

    def intersect_from_line_through(self, a, b):
        """ return intersection with line passing points a and b """
        mdota, mdotb = a.dist_to_plane(self), b.dist_to_plane(self)
        if abs((denom := mdota - mdotb) / (abs(mdota)+abs(mdotb))) < eps:
            return
        return a.lerp(b, mdota / denom)

    @classmethod
    def from_two_vectors_and_point(self, u, v, p):
        """ cross product of u and v defines normal vector and through p """
        (a, b, c), (x, y, z) = u.cross(v).norm(), p
        return plane(a, b, c, -(a * x + b * y + c * z))

    def draw(self):
        x, y = np.linspace(-5, 5, 10), np.linspace(-5, 5, 10)
        X, Y = np.meshgrid(x, y)
        Z = (self.a * X + self.b * Y + self.d) / -self.c
        plt.gca().plot_surface(X, Y, Z, alpha=0.3, cmap='viridis')


if __name__ == '__main__':
    ax = plt.gcf().add_subplot(111, projection='3d')
    ax.set_xlim(0., 1.)
    ax.set_ylim(0., 1.)
    ax.set_zlim(0., 1.)
    ax.set_box_aspect([1., 1., 1.])

    A = point(0, 0, 0)
    adir = point(1, 1, 1)
    B = point(1, 0.0, 0.0)
    bdir = point(0, 0, 1)
    pA, pB = point.line_line_closest_point3d(adir, A, bdir, B)

    A.draw()
    B.draw()
    A.draw_line(A + adir)
    B.draw_line(B + bdir)

    pA.draw()
    pA.draw()
    pB.draw()
    pA.draw_line(pB)

    plt.tight_layout()
    plt.show()
