import random
import matplotlib.pyplot as plt
import networkx as nx
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout


class max_independent_set_for_tree:
    def __init__(self, g):
        self.g = g
        self.checked = [v for v in g.nodes() if g.degree(v) == 1]
        self.T = self.__init_table()
        self.waiting = self.__init_waiting_stack()
        self.__solve()

    def __init_table(self):
        tbl = {(v, True): (v,) for v in self.checked}
        tbl.update({(v, False): () for v in self.checked})
        return tbl

    def __init_waiting_stack(self):
        waiting = []
        for u in self.checked:
            v = self.__find_tbp(u)
            if v is not None and v not in waiting:
                waiting.append(v)
        return waiting

    def __find_tbp(self, v):
        nbr = [w for w in self.g[v] if w not in self.checked]
        if len(nbr) == 1:
            return nbr[0]

    def __solve(self):
        while self.waiting:
            v = self.waiting.pop(0)
            self.__update_tbl(v)
            self.__update_stack(v)

        root = self.checked[-1]
        t, f = self.T[(root, True)], self.T[(root, False)]
        self.__is = t if self.__e(t) > self.__e(f) else f

    def __update_tbl(self, v):
        target = [w for w in self.g[v] if w in self.checked]

        self.T[(v, True)] = (v,)
        for w in target:
            self.T[(v, True)] += self.T[(w, False)]

        self.T[(v, False)] = ()
        for w in target:
            t, f = self.T[(w, True)], self.T[(w, False)]
            self.T[(v, False)] += t if self.__e(t) > self.__e(f) else f

        for w in target:
            del self.T[(w, True)]
            del self.T[(w, False)]

    def __update_stack(self, v):
        w = self.__find_tbp(v)
        if w is not None and w not in self.waiting:
            self.waiting.append(w)
        self.checked.append(v)

    def __e(self, tup):     # weight estimation
        return sum(self.g.node[v]['w'] for v in tup)

    @property
    def independent_set(self):
        return self.__is


def gen():
    g = nx.balanced_tree(3, 4)
    random.seed(8)
    mean = 50.0
    r = [random.expovariate(1. / mean) for i in g.nodes()]
    for v in g.nodes():
        g.node[v]['w'] = r[v]
    return g


if __name__ == '__main__':
    g = gen()
    the = max_independent_set_for_tree(g)
    iset = the.independent_set

    pos = graphviz_layout(g, prog='twopi', args='')
    ns = [g.node[v]['w'] for v in g.nodes()]
    nx.draw(g, pos, node_size=ns, alpha=.5, node_color='b', with_labels=False)
    ns = [g.node[v]['w'] for v in iset]
    nx.draw_networkx_nodes(g, pos, node_size=ns, node_color='g',
                           nodelist=iset, alpha=.75)
    plt.axis('equal')
    plt.savefig('independent_set_on_tree.png', bbox_inches='tight')
    plt.show()
