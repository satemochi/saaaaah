from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import networkx as nx
import numpy as np


def ecc_color(g, e=None, c=cm.rainbow):
    if not e:
        e = nx.eccentricity(g)
    d, r = nx.diameter(g, e=e), nx.radius(g, e=e)
    return c(list(map(lambda x: (x-r)/(d-r), (e[v] for v in g))))


def draw_barycenter(g, pos, ns):
    nx.draw_networkx_nodes(g, pos, node_size=ns, node_color='w', alpha=0.5,
                           nodelist=nx.barycenter(g))


def set_color_bar(cmap, _min, _max):
    sm = cm.ScalarMappable(cmap=cmap)
    sm._A = []
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes('right', size='2%', pad='1%')
    cbar = plt.colorbar(sm, cax=cax, ticks=np.linspace(0, 1, _max-_min+1))
    cbar.ax.set_yticklabels(range(_min, _max+1))


if __name__ == '__main__':
    n = 21
    g = nx.grid_2d_graph(n, n)
    pos = {v: v for v in g}

    c = cm.rainbow_r
    e = nx.eccentricity(g)
    colors = ecc_color(g, e=e, c=c)

    ns = 60
    nodes = nx.draw_networkx_nodes(g, pos, node_size=ns, node_color=colors)
    nodes.set_edgecolor('black')
    nx.draw_networkx_edges(g, pos)
    # draw_barycenter(g, pos, ns)

    diameter, radius = nx.diameter(g, e=e), nx.radius(g, e=e)
    plt.gca().set_aspect('equal')

    set_color_bar(c, radius, diameter)

    print(f'diameter: {diameter}')
    print(f'radius: {radius}')
    plt.savefig('grid_eccentricity.png', bbox_inches='tight')

    plt.tight_layout()
    plt.show()
