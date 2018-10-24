import sys
import matplotlib.cm as cm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    n = 50
    pts = np.random.random((n, 2))     # uniformly distributed in unit square
    weights = np.random.uniform(1., 3., n)    # sampling from [0, 0.1)
    for (x, y), w in zip(pts, weights):
        draw_cone(x, y, w)
    glutSwapBuffers()


def draw_cone(x, y, w):
    glColor4f(*(cm.nipy_spectral((x*x + y*y) / 2.)))    # colored by distance
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)     # apex
    t = np.linspace(0, 2 * np.pi, num=64, endpoint=True)
    radius = np.sqrt(2)
    base_x, base_y = x + radius * np.cos(t), y + radius * np.sin(t)
    for xi, yi in zip(base_x, base_y):
        glVertex3f(xi, yi, radius / w)     # base circle
    glEnd()

    # draw apex point
    glColor4f(1., 1., 1., 1.)
    glBegin(GL_POINTS)
    glVertex3f(x, y, -1)
    glEnd()

    glRasterPos2f(x+0.003, y+0.003)
    for c in str(round(w, 2)):
#        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))


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
    if key == 's':
        glReadBuffer(GL_FRONT)
        w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        buf = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
        img = Image.frombytes(mode="RGB", size=(w, h), data=buf)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save('mw_vor.png')
        print 'saved'


if __name__ == '__main__':
    glutInit(sys.argv)

    # window settings
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("multiplicativelyy weighted Voronoi drawing")

    # to enable hidden surface elimination and so on
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # to enable anti-aliasing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(4)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()
