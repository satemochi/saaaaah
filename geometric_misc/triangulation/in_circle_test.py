from matplotlib import pyplot as plt


class circle:
    def __init__(self, pts):
        assert(len(pts) == 3)
        self.__cx, self.__cy, self.__r = self.__a3(pts)

    @staticmethod
    def __a3(pts):
        (x0, y0), (x1, y1), (x2, y2) = pts

        x01, x02 = x0 - x1, x0 - x2
        y01, y02 = y0 - y1, y0 - y2

        y20, y10 = y2 - y0, y1 - y0
        x20, x10 = x2 - x0, x1 - x0

        sx02, sy02 = x0*x0 - x2*x2, y0*y0 - y2*y2
        sx10, sy10 = x1*x1 - x0*x0, y1*y1 - y0*y0

        f = (sx02*x01+sy02*x01 + sx10*x02+sy10*x02) / (2*(y20*x01 - y10*x02))
        g = (sx02*y01+sy02*y01 + sx10*y02+sy10*y02) / (2*(x20*y01 - x10*y02))
        c = -x0*x0 - y0*y0 - 2*g*x0 - 2*f*y0

        return (-g, -f, (f*f + g*g - c)**0.5)

    def draw(self, c='g', ax=None):
        if ax is None:
            ax = plt.gca()
        c = plt.Circle((self.__cx, self.__cy), self.__r, fill=False, color=c)
        ax.add_artist(c)

    def contains(self, x, y):
        return ((x-self.__cx)**2 + (y-self.__cy)**2)**0.5 <= self.__r + 1e-9


def ccw(p, q, r):
    (px, py), (qx, qy), (rx, ry) = p, q, r
    return ((qx - px) * (ry - py) - (qy - py) * (rx - px)) > 0


def in_circle(a, b, c, d):
    if ccw(a, b, c):
        b, c = c, b
    assert(not ccw(a, b, c))
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = a, b, c, d
    x_ad, y_ad = ax-dx, ay-dy
    x_bd, y_bd = bx-dx, by-dy
    x_cd, y_cd = cx-dx, cy-dy
    sa, sb, sc, sd = ax**2 + ay**2, bx**2 + by**2, cx**2 + cy**2, dx**2 + dy**2
    s1, s2, s3 = sa-sd, sb-sd, sc-sd
    det = (x_ad * y_bd * s3) + (x_bd * y_cd * s1) + (x_cd * y_ad * s2)
    det -= (s1 * y_bd * x_cd) + (s2 * y_cd * x_ad) + (s3 * y_ad * x_bd)
    return det < 0


pts = []


def onclick(event):
    pts.append((event.xdata, event.ydata))
    plt.cla()
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 1)
    plt.scatter([x for x, _ in pts], [y for _, y in pts], zorder=5)
    if len(pts) == 4:
        print(in_circle(*pts))
        circle(pts[:3]).draw()
        c = 'r' if in_circle(*pts) else 'g'
        plt.plot([x for x, _ in pts], [y for _, y in pts], c)
        pts.clear()
    plt.draw()


if __name__ == '__main__':
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 1)
    plt.tight_layout()
    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()
