import subprocess
import japanmap as jp
import pickle
import mpl_toolkits.mplot3d as a3
from matplotlib import pyplot as plt
import numpy as np
from sumo_wrestler import sekitori


def get_pts():
    with open('japan.p2.pkl', 'rw') as f:
        return jp.pref_points(pickle.load(f))


def draw_pref(ax, pts, color='#ffcccc'):
    b = [(x, y, z) for (x, y), z in zip(pts, [0.] * len(pts))]
    face = a3.art3d.Poly3DCollection([b], facecolor=color, edgecolor='k')
    ax.add_collection3d(face)


def draw_box(ax, pts, h, w=.05):
    x, y = np.average(pts, axis=0)
    cx, cy = [x-w, x+w, x+w, x-w], [y-w, y-w, y+w, y+w]
    a, b = zip(cx, cy, [h] * 4), zip(cx, cy, [0] * 4)
    f = [(b[i], b[(i+1) % 4], a[(i+1) % 4], a[i]) for i in xrange(4)]
    side = a3.art3d.Poly3DCollection(f, facecolor='g', edgecolor='darkgreen')
    ax.add_collection3d(side)


def draw(seki, pts):
    ax = a3.Axes3D(plt.figure())
    ax.set_xlim(127, 146)
    ax.set_ylim(26, 46)
    ax.set_zlim(0, max(len(seki[i]) for i in xrange(47)) + 1)

    for pid in range(47):
        draw_pref(ax, pts[pid])
        draw_box(ax, pts[pid], len(seki[pid]))


def make_gif():
    for i in xrange(0, 360, 9):
        plt.gca().view_init(azim=i)
        plt.savefig('a3_' + str(i).zfill(3) + '.png', bbox_inches='tight')
    cmd = 'convert -delay 20 -layers Optimize a3_*.png a3.gif'
    subprocess.call(cmd, shell=True)
    subprocess.call('rm a3_*.png', shell=True)


if __name__ == '__main__':
    draw(sekitori(), get_pts())
    make_gif()
