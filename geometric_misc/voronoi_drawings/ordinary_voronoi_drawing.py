import sys
import matplotlib.cm as cm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    pts = np.random.random((50, 2))
    for x, y in pts:
        draw_cone(x, y)
    glutSwapBuffers()


def draw_cone(x, y):
    glColor4f(*(cm.nipy_spectral((x*x + y*y) / 2.)))
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(x, y, 0)
    t = np.linspace(0, 2 * np.pi, num=64, endpoint=True)
    radius = np.sqrt(2)
    base_x, base_y = x + radius * np.cos(t), y + radius * np.sin(t)
    for xi, yi in zip(base_x, base_y):
        glVertex3f(xi, yi, radius)
    glEnd()

    glColor4f(0., 0., 0., 1.)
    glBegin(GL_POINTS)  # draw apex point
    glVertex2f(x, y)
    glEnd()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, 1.0, -1.0)  # l, r, b, t, -near, -far
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard(key, x, y):
    if key == '\033' or key == 'q':
        sys.exit()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("ordinary Voronoi drawing")
    glEnable(GL_DEPTH_TEST)     # to enable hidden surface elimination
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glPointSize(3)
    glutMainLoop()
