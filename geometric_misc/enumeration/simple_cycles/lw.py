from collections import defaultdict, deque
from functools import reduce
import networkx as nx


class fc:
    """ Enumeration simple cycles in an undirected graph based on
        breadth-first-searching (analogous to finding girth, I think).
        - Reference:
            Liu & Wang (2006): ``A new way to enumerate cycles in graph'' """
    def __init__(self, g):
        self.__g = g
        self.__ref(g)

    def __ref(self, g):
        self.__o = {v: i for i, v in enumerate(g)}
        self.__ei, self.__ie = {}, {}
        for i, (u, v) in enumerate(g.edges):
            self.__ei[u, v], self.__ei[v, u], self.__ie[i] = i, i, (u, v)

    def iter_cycles(self):
        q, cl = deque(((v, v, 0, 1 << self.__o[v]) for v in self.__g)), set()
        while q:
            h, t, ec, vc = q.popleft()
            if self.__g.has_edge(h, t):
                s = nx.Graph([self.__ie[i] for i in self.__elem(ec)]+[(h, t)])
                if (y := ec + (1 << self.__ei[h, t])) not in cl:
                    try:
                        yield next(self.__iter_fc(s))
                        cl.add(y)
                    except StopIteration:
                        pass
            for x in self.__g[t]:
                if self.__o[x] < self.__o[h] or (vc >> self.__o[x]) & 1:
                    continue
                q.append((h, x, ec + (1 << self.__ei[t, x]),
                          vc + (1 << self.__o[x])))

    @staticmethod
    def __elem(b):
        return [i for i in range(b.bit_length()+1) if (b >> i) & 1]

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


def gen():
    return nx.frucht_graph()
    return nx.house_x_graph()


if __name__ == '__main__':
    g = gen()
    print(len(list(fc(g).iter_cycles())))

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
