from itertools import product
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def laplacian_embedding(g):
    lap = nx.normalized_laplacian_matrix(g)
    eig_w, eig_v = np.linalg.eig(lap.toarray())
    second_vector = eig_v[:, eig_w.argsort()][-2]
    return {v: (second_vector[v], 0) for v in g}


def draw_edges_linearly(g, pos):
    for u, v in g.edges:
        __de(pos[u][0], pos[v][0])


def __de(x1, x2):
    _a, _x = 0.2, np.linspace(0, (j := max(x1, x2)) - (i := min(x1, x2)), 100)
    plt.plot(i+_x, _a * (j - i) * np.sin(np.pi*_x/(j-i)),
             c='b', zorder=-10, alpha=0.3)


def sparsest_cut_with_spectral_method(g):
    le = laplacian_embedding(g)
    lv = [v for x, v in sorted((x, v) for v, (x, _) in le.items())]
#    return min((__sparsity(g, lv[:i], lv[i:]), i, lv[:i])
#               for i in range(1, g.order()))[2]
    return min((__sparsity(g, lv[:i], lv[i:]), i, lv[:i])
               for i in range(1, g.order()))


def __sparsity(g, s, t):
    return sum(1 for e in product(s, t) if g.has_edge(*e)) \
                / min(len(s), len(t))


if __name__ == '__main__':
    g = nx.frucht_graph()
#    g = nx.path_graph(6)

    pos = laplacian_embedding(g)

    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc', node_size=33)
    nodes.set_edgecolor('k')

    (c, _, s) = sparsest_cut_with_spectral_method(g)
    print(c)
    plt.title(f'sparsity: {c}')
    nodes = nx.draw_networkx_nodes(g, pos, nodelist= s,
                                   node_color='#ccffcc', node_size=33)
    nodes.set_edgecolor('k')

    draw_edges_linearly(g, pos)
    lpos = {v: (x, y-0.03) for v, (x, y) in pos.items()}
    nx.draw_networkx_labels(g, lpos, font_size=9)

    e = 1e-2
    xmin = min(x for x, y in pos.values())
    xmax = max(x for x, y in pos.values())
    plt.gca().set_xlim(xmin-e, xmax+e)
    plt.gca().set_ylim(-0.2, 0.2)

    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.tight_layout()
    # plt.savefig('spectral_partition_on_frucht_graph.png', bbox_inches='tight')
    plt.show()
