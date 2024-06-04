import sys
sys.path.append('..')
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from line_intersections import line_intersections


def get_pos(g):
    x, y = nx.bipartite.sets(g)
    m = len(x)-1 if (len(x)-1) % 2 == 1 else len(x)+1
    n = len(y)-1 if (len(y)-1) % 2 == 1 else len(y)+1
    dx, dy = 4/m, 2/n
    pos = {}

    xi = iter([-2+dx*i for i in range(m+1)])
    for i, v in enumerate(x):
        dx = next(xi)
        if m & 1 == 0 and i == m//2:
            dx = next(xi)
        pos[v] = (dx, 0)

    yi = iter([-1+dy*i for i in range(n+1)])
    for i, v in enumerate(y):
        dy = next(yi)
        if n & 1 == 0 and i == n//2:
            dy = next(yi)
        pos[v] = (0, dy)

    return pos


def get_segs(g, pos):
    return [__seg(pos[u], pos[v]) for u, v in g.edges]


def __seg(p1, p2):
    xs, ys = np.linspace(*p1), np.linspace(*p2)
    return ((xs[1], ys[1]), (xs[-2], ys[-2]))


if __name__ == '__main__':
    m, n = 9, 6
    g = nx.complete_bipartite_graph(m, n)
    pos = get_pos(g)

    # nx.draw_networkx_labels(g, pos, font_size=9)
    # nodes = nx.draw_networkx_nodes(g, pos, node_size=160, nodelist=a,

    ns = 60
    a, b = nx.bipartite.sets(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_size=ns, nodelist=a,
                                   node_color='#0087ff')
    nodes.set_edgecolor('k')
    nodes = nx.draw_networkx_nodes(g, pos, node_size=ns, nodelist=b,
                                   node_color='#ffdf00')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, alpha=0.25)

    for x, y in line_intersections(get_segs(g, pos)).search():
        plt.scatter([x], [y], c='#cc3333', s=5)

    e = 0.1
    plt.gca().set_xlim(-2-e, 2+e)
    plt.gca().set_ylim(-1-e, 1+e)
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    #plt.savefig('turan_brick_factory_01.png', bbox_inches='tight', dpi=200)
    plt.show()
