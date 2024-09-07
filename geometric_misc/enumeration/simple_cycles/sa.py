from functools import reduce
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


class fc:
    def __init__(self, g):
        self.__g, self.__ei = g, {}
        for i, (u, v) in enumerate(g.edges):
            self.__ei[u, v], self.__ei[v, u] = i, i
        self.__c = [nx.cycle_graph(i) for i in range(3, g.order()+1)]

    def iter_cycles(self):
        for ci in self.__c:
            cl, m = set(), GraphMatcher(self.__g, ci)
            for f in m.subgraph_monomorphisms_iter():
                i = {v: k for k, v in f.items()}
                if (cc := self.__ec((cv := [i[v] for v in ci]))) in cl:
                    continue
                yield cv
                cl.add(cc)

    def __ec(self, c):
        return reduce(lambda x, i: x + (1 << self.__ei[i]), zip(c, c[1:]),
                      1 << self.__ei[c[-1], c[0]])


def gen():
    return nx.frucht_graph()
    return nx.house_x_graph()


if __name__ == '__main__':
    g = gen()
    print(len(list(fc(g).iter_cycles())), len(list(nx.simple_cycles(g))))

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g, seed=1)
    for c in fc(g).iter_cycles():
        nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw_networkx_labels(g, pos)

        plt.gca().set_aspect('equal')
        plt.gca().axis('off')
        el = [(u, v) for u, v in zip(c, c[1:])] + [(c[-1], c[0])]
        nx.draw_networkx_edges(g, pos, edgelist=el, edge_color='g', width=2)
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
        plt.cla()
    plt.show()
