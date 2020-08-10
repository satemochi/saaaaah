import networkx as nx


def random_greedy_spanner(g, t=2):
    from heapq import heapify, heappop
    stack = [(_norm(*u, *v), (u, v)) for u, v in g.edges]
    heapify(stack)
    gs = nx.Graph()
    gs.add_nodes_from(g)
    while stack:
        _, (u, v) = heappop(stack)
        d_uv = _norm(*u, *v)
        if nx.has_path(gs, u, v):
            if t * d_uv < nx.shortest_path_length(gs, u, v, 'weight'):
                gs.add_edge(u, v, weight=d_uv)
        else:
            gs.add_edge(u, v, weight=d_uv)
    return gs


def _norm(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5


def gen(n, s):
    from random import random, seed
    from itertools import combinations
    seed(s)
    return nx.Graph(combinations(((random(), random()) for i in range(n)), 2))


if __name__ == '__main__':
    g = gen(n:=50, s:=0)

    pos = {v: v for v in g}
    nx.draw_networkx_nodes(g, pos, node_size=50, alpha=0.75, with_labels=False)
    nx.draw_networkx_edges(g, pos, alpha=0.051)

    gs = random_greedy_spanner(g, 2)
    nx.draw_networkx_edges(gs, pos, edge_color='#ff4444', width=2)

    print(g.size(), gs.size())

    from matplotlib import pyplot as plt
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    # plt.savefig('random_greedy_spanner_01.png', bbox_inches='tight', dpi=150)
    plt.tight_layout()
    plt.show()
