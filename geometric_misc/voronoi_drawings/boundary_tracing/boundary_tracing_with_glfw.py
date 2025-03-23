from math import cos, pi, sin
from random import random, seed, uniform
import cv2
import glfw
import numpy as np
from OpenGL.GL import *


class site:
    def __init__(self, x, y, w, c, win_w, win_h):
        self.x, self.y, self.w, self.c = x, y, w, c
        self.ww, self.wh = win_w, win_h
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
        gx, gy = int(self.ww * self.x), int(self.wh * self.y)
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
        gx, gy = int(self.ww * self.x), int(self.wh * self.y)
        for x in range(gx, -1, -1):
            if img[gy][x] != self.c[0]:
                return (x+1, gy)
        return (0, gy)

    def __check_valid_image_boundaries(self, img, next_x, next_y):
        if (next_y >= self.wh or next_x < 0 or next_y < 0
            or next_x >= self.ww):
            return False
        if img[next_y][next_x] == self.c[0]:
            return True


def setup(w, h):
    glViewport(0, 0, w, h)
    glOrtho(0.0, 1.0, 0.0, 1.0, 1.0, -1.0)  # l, r, b, t, -near, -far
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)


def draw(sites, w, h):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for s in sites:
        s.draw()
    buf = glReadPixels(0, 0, w, h, GL_RED, GL_UNSIGNED_BYTE)
    image = np.frombuffer(buf, dtype=np.uint8).reshape(w, h)
    glColor3ub(255, 255, 255)
    for s in sites:
        glBegin(GL_LINE_LOOP)
        for x, y in s.get_boundary(image):
            glVertex3d(x / w, y / h, -1)
        glEnd()


def save(w, h):
    image_buffer = glReadPixels(0, 0, w, h, GL_BGR, GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(w, h, 3)[::-1]
    cv2.imwrite("boundary_tracing_with_glfw.png", image)


def gen(n, cmap, win_w, win_h):
    seed(2)
    return [site(random(), random(), uniform(0, 0.1), cmap[i], win_w, win_h)
            for i in range(n)]


if __name__ == "__main__":
    cmap = ((153, 0, 0), (175, 97, 16), (191, 144, 0), (56, 118, 29),
            (19, 79, 92))
    w, h = 1200, 1200
    sites = gen(5, cmap, w, h)

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, False)
    window = glfw.create_window(w, h, "hidden window", None, None)
    glfw.make_context_current(window)

    setup(w, h)
    draw(sites, w, h)
    save(w, h)
#    glfw.swap_buffers(window)
#    while not glfw.window_should_close(window):
#        glfw.poll_events()
    glfw.destroy_window(window)
    glfw.terminate()
