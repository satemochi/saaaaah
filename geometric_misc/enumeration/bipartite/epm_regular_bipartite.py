from random import seed
from matplotlib import pyplot as plt
import networkx as nx


def bipartite_regular_graph(g):
    assert(nx.is_regular(g))
    d = nx.DiGraph(nx.eulerian_circuit(g))
    return nx.Graph([(u, g.order()+v) for u, v in d.edges])


def perfect_matching_iter(g):
    assert(nx.is_bipartite(g) and nx.is_regular(g))
    from pprint import pprint

    a, _ = nx.bipartite.sets(g)
    m = [(v, (mm := nx.bipartite.hopcroft_karp_matching(g))[v]) for v in a]
    yield m
    stack = [(g, m, ())]
    while stack:
        h, m, preserved = stack.pop()
        domain = a & set(h)
        d = nx.DiGraph([(u, v) if (u, v) in m else (v, u)
                        for u in domain for v in h[u]])
        try:
            n = len(c := next(nx.simple_cycles(d)))
        except(StopIteration):
            continue
        new = ([(c[(i + 1) % n], u) for i, u in enumerate(c) if u not in a] +
               [(u, v) for u in domain for v in d[u]
                if u not in c and v not in c])
        yield (nm := new + list(preserved))

        e = next(e0 for i in range(n) if (e0 := (c[i], c[(i + 1) % n])) in m)
        gp, gm = h.copy(), h.copy()
        gp.remove_nodes_from(e)
        gm.remove_edge(*e)
        stack += [(gp, m, preserved+(e,)), (gm, nm, preserved)]


def gen(n, d):
    return nx.random_regular_graph(d, n)


if __name__ == '__main__':
    seed(0)
    g = gen(n := 10, d := 6)
    b = bipartite_regular_graph(g)

    pos = nx.spring_layout(b)
    for i, pm in enumerate(perfect_matching_iter(b)):
        print(i,)
        plt.gca().cla()
        nx.draw_networkx_edges(g, pos, alpha=0.1)
        nx.draw_networkx_edges(b, pos)
        nx.draw_networkx_edges(b, pos, edgelist=pm, edge_color='r')
        nx.draw_networkx_labels(b, pos)
        l, r = nx.bipartite.sets(b)
        nx.draw_networkx_nodes(b, pos, nodelist=l, node_color='#ffcccc')
        nx.draw_networkx_nodes(b, pos, nodelist=r, node_color='#ccffcc')

        plt.gca().set_aspect('equal')
        plt.gca().axis('off')
        plt.autoscale()
        plt.tight_layout()
        plt.draw()
        plt.pause(0.5)

    plt.savefig('perfect_matching_on_regular_bipartite_01.png',
                bbox_inches='tight')
    plt.show()
