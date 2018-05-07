import pickle
import random
import japanmap as jp
import mpl_toolkits.mplot3d as a3
from matplotlib import pyplot as plt


def get_pts():
    with open('japan.p2.pkl', 'rw') as f:
        return jp.pref_points(pickle.load(f))


def draw_pref(ax, pts, pid, height=20., color='#ffcccc'):
    n = len(pts[pid])
    top = [(x, y, z) for (x, y), z in zip(pts[pid], [height] * n)]
    bot = [(x, y, z) for (x, y), z in zip(pts[pid], [0.] * n)]
    tface = a3.art3d.Poly3DCollection([top])
    tface.set_facecolor(color)
    tface.set_edgecolor('k')

    facets = [[bot[i], bot[(i+1)%n], top[(i+1)%n], top[i]] for i in xrange(n)]
    sides = a3.art3d.Poly3DCollection(facets, linewidths=1, alpha=0.1)
    sides.set_facecolor(color)
    sides.set_edgecolor('k')
    sides.set_alpha(0.001)

    ax.add_collection3d(sides)
    ax.add_collection3d(tface)


if __name__ == '__main__':
    ax = a3.Axes3D(plt.figure())

    pts = get_pts()
    for pid in range(47):
        draw_pref(ax, pts, pid, height=random.uniform(0., .1),
                  color='#ffcccc')

    ax.set_xlim(127, 146)
    ax.set_ylim(26, 46)
    ax.set_zlim(0, 0.2)

    plt.show()

