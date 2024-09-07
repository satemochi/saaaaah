from collections import defaultdict
from functools import reduce
import networkx as nx


class fc:
    """ Enumeration for simple cycles in a undirected graph based on
        the cycle vector space due to Keith PATON in 1969.

        Reference:
            Philipp Sch: ``Enumerating All Cycles in an Undirected Graph'' """
    def __init__(self, g):
        self.__fc = list(self.__iter_fc(g))
        self.__ref(g)

    def __iter_fc(self, g):
        d, s = defaultdict(lambda: -1), [((r := next(iter(g))), iter(g[r]))]
        d[r], p = 0, {r: r}
        while s:
            x, children = s[-1]
            try:
                y = next(children)
                if d[y] < 0:  # tree edge
                    d[y], p[y] = d[x] + 1, x
                    s.append((y, iter([u for u in g[y] if u != x])))
                else:
                    if d[x] > d[y]:  # back edge
                        c = [x]
                        while x != y:
                            c.append((x := p[x]))
                        yield c
            except StopIteration:
                s.pop()

    def __ref(self, g):
        self.__ei, self.__ie = {}, {}
        for i, (u, v) in enumerate(g.edges):
            self.__ei[u, v], self.__ei[v, u], self.__ie[i] = i, i, (u, v)
        self.__fcc = {i: self.__ec(c) for i, c in enumerate(self.__fc)}

    def __ec(self, c):
        return reduce(lambda x, i: x + (1 << self.__ei[i]), zip(c, c[1:]),
                      1 << self.__ei[c[-1], c[0]])

    def iter_cycles(self):
        for i in range(1, 1 << (len(self.__fc))):
            if len((ci := self.__elem(i))) == 1:
                yield self.__fc[ci[0]]
            elif all(any(self.__fcc[c1] & self.__fcc[c2]
                         for c2 in ci if c1 != c2) for c1 in ci):
                xo = reduce(lambda x, i: x ^ self.__fcc[i], ci, 0)
                s = nx.Graph([self.__ie[i] for i in self.__elem(xo)])
                try:
                    new = next(self.__iter_fc(s))
                    if len(new) == s.order():
                        yield new
                except StopIteration:
                    pass

    @staticmethod
    def __elem(b):
        return [i for i in range(b.bit_length()+1) if (b >> i) & 1]


def gen():
    return nx.house_x_graph()
    return nx.frucht_graph()


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
        plt.pause(0.5)
        plt.cla()
    plt.show()
