from itertools import combinations
from random import random, seed
from matplotlib import pyplot as plt
import networkx as nx


def randcons_3spanner(g, s=None):
    seed(s)
    clusters, parent, delta = {}, {}, g.order()**-0.5
    while len(clusters) < 1:
        clusters = {u: {u} for u in g if random() < delta}

    E_spanner = []
    for u in g:
        if u in clusters:
            continue
        if not set(g[u]) & set(clusters):
            E_spanner += [(u, v) for v in g[u]]
        else:
            parent[u] = (nn:=min((g[u][c]['weight'], c) for c in clusters)[1])
            clusters[nn].add(u)
            E_spanner.append((u, nn))
            weight = g[u][nn]['weight']
            E_spanner += [(u, v) for v in g[u] if g[u][v]['weight'] < weight]

    E_dash = [(u, v) for u, v in g.edges
              if (not (u in clusters and v in clusters) and
                  not (u in parent and v in parent and parent[u] == parent[v]))]

    gd = nx.Graph(E_dash)
    for v in gd:
        for _, c in clusters.items():
            if v in c or not set(gd[v]) & c:
                continue
            nn = min((g[v][w]['weight'], w) for w in gd[v] if w in c)[1]
            E_spanner.append((v, nn))
    return clusters, E_spanner



def gen(n, s):
    seed(s)
    g = nx.Graph()
    for p, q in combinations(((random(), random()) for i in range(n)), 2):
        (x0, y0), (x1, y1) = p, q
        g.add_edge(p, q, weight=((x0-x1)**2+(y0-y1)**2)**0.5)
    return g


if __name__ == '__main__':
    g = gen(n:=36, s:=1)

    pos = {p: p for p in g}
    nx.draw_networkx(g, pos, node_color='g', node_size=30,
                     with_labels=False, alpha=0.2)
    # c, es = randcons_3spanner(g, s)
    c, es = randcons_3spanner(g)
    nx.draw_networkx_nodes(g, pos, nodelist=list(c), node_size=100,
                           node_color='g')
    nx.draw_networkx_edges(g, pos, edgelist=es, edge_color='b')

    print(g.size(), len(es), n**1.5)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('3-spanner_ex1.png', bbox_inches='tight')
    plt.show()
