from collections import defaultdict
from matplotlib import pyplot as plt
import networkx as nx


def dense_subgraph_2_approx(g):
    res = (density(g, g.nodes), g.nodes)
    s = {v: d for v, d in g.degree()}
    dt = defaultdict(set)
    for v, d in s.items():
        dt[d].add(v)
    d_min = min(dt)

    while s:
        if not dt[d_min]:
            d_min = min(d for d in dt if dt[d])
        v = dt[d_min].pop()
        del s[v]
        for u in g[v]:
            if u not in s:
                continue
            dt[s[u]].discard(u)
            s[u] -= 1
            dt[s[u]].add(u)
            d_min = s[u] if not dt[d_min] else min(d_min, s[u])
        if res < (_ := density(g, s), 0):
            res = (_, list(s))
    return res


def density(g, s):
    return 0 if not s else g.subgraph(s).size() / len(s)


def __gen(n=20, r=0.2, s=0):
    return nx.random_geometric_graph(n, r, seed=s)


if __name__ == '__main__':
    g = __gen()
    print(density(g, g.nodes))
    dens, s = dense_subgraph_2_approx(g)
    print(dens)

    pos = nx.get_node_attributes(g, 'pos')
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc', node_size=50)
    nodes.set_edgecolor('k')
    nodes = nx.draw_networkx_nodes(g, pos, nodelist=s, node_color='#aaffaa',
                                   node_size=50)
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
