from itertools import combinations
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def kneser_graph(n, k):
    edges = [(x, y) for x, y in combinations(combinations(range(n), k), 2)
             if not set(x) & set(y)]
    return nx.Graph(edges)


def draw_kneser(g, n, s=20):
    pos = nx.nx_agraph.graphviz_layout(g, prog='dot')
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    nx.draw_networkx_nodes(g, pos, alpha=0.15, node_size=250, node_color='r')
    for v in g:
        draw_node(v, n, s, *pos[v])


def draw_node(nodes, n, s, x, y):
    c = ['r' if i in nodes else 'g' for i in range(n)]
    t = np.linspace(0, 2*np.pi, n+1)
    cx = [x + s * np.cos(ti) for ti in t[:-1]]
    cy = [y + s * np.sin(ti) for ti in t[:-1]]
    plt.scatter(cx, cy, c=c, s=10)


if __name__ == '__main__':
    n, k = 7, 3
    g = kneser_graph(n, k)

    print(f'n: {n}, k: {k}')
    print(f'v: {g.order()}, e: {g.size()}')
    print([round(c.real) for c in nx.adjacency_spectrum(g)])

    draw_kneser(g, n)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig('kneser_graph_7_3.png', bbox_inches='tight')
    plt.show()
