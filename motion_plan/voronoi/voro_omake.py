import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, cKDTree


def redraw():
    global vor
    plt.cla()
    voronoi_plot_2d(vor, ax=plt.gca(), show_vertices=False)
    plt.gca().set_xlim([0, 1])
    plt.gca().set_ylim([0, 1])


def onclick(event):
    global pts, vor, voronoi_kdtree
    if event.xdata is not None:
        redraw()
        dist, idx = voronoi_kdtree.query([event.xdata, event.ydata], k=7)
        poly = [vor.vertices[i] for i in vor.regions[vor.point_region[idx[0]]]]
        plt.fill(*zip(*poly), alpha=0.3, color='g')
        plt.plot([pts[i][0] for i in idx], [pts[i][1] for i in idx], 'ro')
        plt.plot([event.xdata], [event.ydata], 'x')
        plt.draw()

pts = [[random.random(), random.random()] for i in range(300)]
pts = pts + [[100, 100], [100, -100], [-100, 0]]

vor = Voronoi(pts)
voronoi_kdtree = cKDTree(pts)

fig = plt.figure(figsize=(6, 6), facecolor='white')
fig.canvas.mpl_connect('button_press_event', onclick)

redraw()
plt.show()
