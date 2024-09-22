from functools import reduce
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def sc_iter(g):
    ei = {}
    for i, (u, v) in enumerate(g.edges):
        ei[u, v], ei[v, u] = i, i

    for ci in iter(nx.cycle_graph(i) for i in range(3, g.order()+1)):
        cl, m = set(), GraphMatcher(g, ci)
        for f in m.subgraph_monomorphisms_iter():
            i = {v: k for k, v in f.items()}
            cv = [i[v] for v in ci]
            cc = reduce(lambda x, e: x + (1 << ei[e]), zip(cv, cv[1:]),
                        1 << ei[cv[-1], cv[0]])
            if cc not in cl:
                yield cv
                cl.add(cc)


def gen():
    return nx.frucht_graph()                    # 83
    return nx.house_x_graph()                   # 12
    return nx.tetrahedral_graph()               # 7
    return nx.truncated_tetrahedron_graph()     # 84
    return nx.chvatal_graph()                   # 1755


if __name__ == '__main__':
    g = gen()
    print(len(list(sc_iter(g))), len(list(nx.simple_cycles(g))))

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g, seed=1)
    for c in sc_iter(g):
        nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw_networkx_labels(g, pos)

        plt.gca().set_aspect('equal')
        plt.gca().axis('off')
        el = tuple(zip(c, c[1:])) + ((c[-1], c[0]),)
        nx.draw_networkx_edges(g, pos, edgelist=el, edge_color='g', width=2)
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
        plt.cla()
    plt.show()
