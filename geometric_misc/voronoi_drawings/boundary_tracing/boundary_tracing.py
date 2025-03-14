from math import cos, pi, sin
from random import random, seed, uniform
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


class site:
    def __init__(self, x, y, w, c=None):
        self.x, self.y, self.w = x, y, w
        self.c = c if c is not None else (0, 0, 0)
        r, ti = 2, 2 * pi / 64
        self.b_coords = [(x+r*cos(ti * i), y+r*sin(ti * i), (z := -w + r))
                         for i in range(64)] + [(x+r, y, z)]

    def draw(self):
        glColor3ubv(self.c)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3d(self.x, self.y, -self.w)     # apex
        for xi, yi, zi in self.b_coords:
            glVertex3d(xi, yi, zi)              # base circle
        glEnd()

    def __repr__(self):
        return f"({self.x}, {self.y}), {self.w}, {self.c}"

    def get_boundary(self, img):
        """ ref.
        https://github.com/Abdelrahmanhassan1/Inner-Boundary-Tracing-Algorithm
        """
        gx, gy = int(600 * self.x), int(600 * self.y)
        assert img[gy][gx] == self.c[0]
        boundaries, d = [self.__find_left_most(img)], 4
        while True:
            d = (d + 6) & 7 if d & 1 else (d + 7) & 7
            while True:
                next_x, next_y = boundaries[-1]
                if d == 0:
                    next_y += 1
                elif d == 1:
                    next_x, next_y = next_x - 1, next_y + 1
                elif d == 2:
                    next_x -= 1
                elif d == 3:
                    next_x, next_y = next_x - 1, next_y - 1
                elif d == 4:
                    next_y -= 1
                elif d == 5:
                    next_x, next_y = next_x + 1, next_y - 1
                elif d == 6:
                    next_x += 1
                elif d == 7:
                    next_x, next_y = next_x + 1, next_y + 1
                if self.__check_valid_image_boundaries(img, next_x, next_y):
                    boundaries.append((next_x, next_y))
                    break
                d = (d + 1) & 7
            if len(boundaries) >= 4:
                if (boundaries[-1] == boundaries[1] and
                        boundaries[-2] == boundaries[0]):
                    break
        return boundaries

    def __find_left_most(self, img):
        gx, gy = int(600 * self.x), int(600 * self.y)
        for x in range(gx, -1, -1):
            if img[gy][x] != self.c[0]:
                return (x+1, gy)
        return (0, gy)

    def __check_valid_image_boundaries(self, img, next_x, next_y):
        if (next_y >= 600 or next_x < 0 or next_y < 0 or next_x >= 600):
            return False
        if img[next_y][next_x] == self.c[0]:
            return True


def gen(n=5):
    seed(2)
    return [site(random(), random(), uniform(0, 0.1), cmap[i])
            for i in range(n)]


""" globals """
cmap = ((153, 0, 0), (175, 97, 16), (191, 144, 0), (56, 118, 29), (19, 79, 92))
sites = gen()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for s in sites:
        s.draw()

    buf = glReadPixels(0, 0, 600, 600, GL_RED, GL_UNSIGNED_BYTE)
    image = np.frombuffer(buf, dtype=np.uint8).reshape(600, 600)
    glColor3ub(255, 255, 255)
    for s in sites:
        glBegin(GL_LINE_LOOP)
        for x, y in s.get_boundary(image):
            glVertex3d(x / 600, y / 600, -1)
        glEnd()
    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glOrtho(0.0, 1.0, 0.0, 1.0, 1.0, -1.0)  # l, r, b, t, -near, -far


if __name__ == '__main__':
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("boundary tracing")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()
