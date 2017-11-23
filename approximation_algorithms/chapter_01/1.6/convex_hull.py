from matplotlib import pyplot as plt
from shapely.geometry import MultiPoint
from descartes.patch import PolygonPatch
import numpy as np


def gen_sequences(n=9, seed=5):
    np.random.seed(seed)
    return (np.random.rand(n), np.random.rand(n))


def plot_config():
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-.1, 1.1)
    plt.gca().set_ylim(-.1, 1.1)
    plt.xlabel('b')
    plt.ylabel('a')
    title_string = 'Fact 1.10:   '
    title_string += r'$\min_i\ \frac{a_i}{b_i} \ \ \leq\ \ $'
    title_string += r'$\frac{\sum_i\ a_i}{\sum_i\ b_i}$'
    plt.title(title_string, y=1.05)


def plot_convex_hull(x, y):
    P = MultiPoint(zip(x, y))
    plt.gca().scatter(x, y, marker='o', color='#6699cc')
    patch = PolygonPatch(P.convex_hull, facecolor='#6699cc',
                         edgecolor='#6699cc', alpha=0.5, zorder=-2)
    plt.gca().add_patch(patch)


def plot_slopes(xdata, ydata):
    xave, yave = np.average(xdata), np.average(ydata)
    plt.gca().scatter([xave], [yave], color='r', zorder=0)

    amin = np.argmin([yi / xi for xi, yi in zip(xdata, ydata)])
    amax = np.argmax([yi / xi for xi, yi in zip(xdata, ydata)])

    x = np.array(plt.gca().get_xlim())
    plt.plot(x, (yave / xave) * x, zorder=-1, label='average', linestyle='--')
    plt.plot(x, (ydata[amin] / xdata[amin]) * x, zorder=-1, label='min', linestyle='--')
    plt.plot(x, (ydata[amax] / xdata[amax]) * x, zorder=-1, label='max', linestyle='--')

    plt.legend(loc='best')

if __name__ == '__main__':
    a, b = gen_sequences()
    np.set_printoptions(precision=3)
    print a
    print
    print b
    plot_config()
    plot_convex_hull(b, a)
    plot_slopes(b, a)

    plt.savefig('fact110_2d_img.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
