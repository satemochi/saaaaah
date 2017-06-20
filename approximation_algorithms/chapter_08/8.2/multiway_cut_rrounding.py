import random
from lpsolve55 import lpsolve, IMPORTANT, Infinite
from matplotlib import pyplot as plt
import networkx as nx
from tutte_pos import tutte_pos


class multiway_cut:
    def __init__(self, g, srcs):
        self.__g = g
        self.__s = srcs
        self.__nv = g.number_of_nodes()
        self.__ne = g.number_of_edges()
        self.__k = len(srcs)
        self.__cutset = []
        self.__randomized_rounding()

    def __set_objective(self, lp):
        coeff = [0] * (self.__nv * self.__k)
        for u, v in self.__g.edges_iter():
            coeff += [self.__g[u][v]['cost']] * self.__k
        lpsolve('set_obj_fn', lp, coeff)

    def __node_constraints(self, lp):
        coeff = [0] * ((self.__nv + self.__ne) * self.__k)
        for v in self.__g.nodes_iter():
            for i in range(self.__k):
                coeff[v * self.__k + i] = 1
            lpsolve('add_constraint', lp, coeff, 'EQ', 1)
            for i in range(self.__k):
                coeff[v * self.__k + i] = 0

    def __edge_constraints(self, lp):
        node_offset = self.__nv * self.__k
        coeff = [0] * ((self.__nv + self.__ne) * self.__k)
        for e, (u, v) in enumerate(self.__g.edges_iter()):
            uk, vk = u * self.__k, v * self.__k
            for i in range(self.__k):
                coeff[node_offset + e * self.__k + i] = 1
                coeff[uk + i] = 1
                coeff[vk + i] = -1
                lpsolve('add_constraint', lp, coeff, 'GE', 0)
                coeff[uk + i] = -1
                coeff[vk + i] = 1
                lpsolve('add_constraint', lp, coeff, 'GE', 0)
                coeff[node_offset + e * self.__k + i] = 0
                coeff[uk + i] = 0
                coeff[vk + i] = 0

    def __constraints(self, lp):
        self.__node_constraints(lp)
        self.__edge_constraints(lp)

    def __bounds(self, lp):
        nv, ne = self.__nv * self.__k, self.__ne * self.__k
        # lpsolve('set_binary', lp, [1] * nv + [0] * ne)
        lpsolve('set_upbo', lp, [1] * nv + [Infinite] * ne)
        lpsolve('set_lowbo', lp, [0] * nv + [0] * ne)
        for i, v in enumerate(self.__s):
            lpsolve('set_lowbo', lp, v * self.__k + i + 1, 1)

    def __config(self, lp):
        lpsolve('set_verbose', lp, IMPORTANT)
        lpsolve('write_lp', lp, 'e.lp')

    def __lin_prog(self):
        lp = lpsolve('make_lp', 0, (self.__nv + self.__ne) * self.__k)
        self.__set_objective(lp)
        self.__constraints(lp)
        self.__bounds(lp)
        self.__config(lp)
        lpsolve('solve', lp)
        return lpsolve('get_variables', lp)[0][:self.__nv * self.__k]

    def __rand_init(self, seed):
        random.seed(seed)
        r = random.random()
        pi = range(self.__k)
        random.shuffle(pi)
        return (r, pi)

    def __B(self, var, i, r):
        ci = []
        for v in range(self.__nv):
            # By lemma 8.5
            if 1 - var[v * self.__k + i] <= r:
                ci.append(v)
        return ci

    def __add_delta(self, C):
        for v in self.__g.nodes_iter():
            for i, c in enumerate(C):
                if v in c:
                    g.node[v]['component'] = self.__s[i]
                    break
        for u, v in self.__g.edges_iter():
            if self.__g.node[u]['component'] != self.__g.node[v]['component']:
                self.__cutset.append((u, v))

    def __component_set(self, var, seed):
        r, pi = self.__rand_init(seed)
        C = [[]] * self.__k
        X = set()
        for i in pi[:-1]:
            ci = set(self.__B(var, i, r)).difference(X)
            X = X.union(ci)
            C[i] = list(ci)
        C[pi[-1]] = list(set(self.__g.nodes()).difference(X))
        return C

    def __randomized_rounding(self, seed=0):
        variables = self.__lin_prog()
        C = self.__component_set(variables, seed)
        self.__add_delta(C)

    def draw(self):
        pos = tutte_pos(g, 1)
        costs = [self.__g[u][v]['cost'] for u, v in self.__g.edges_iter()]

        nx.draw_networkx(self.__g, pos=pos, node_color='#ffddaa',
                         edge_color='#cccccc', node_size=150,
                         font_size=8, width=costs)
        nx.draw_networkx_nodes(self.__g, pos=pos, nodelist=srcs,
                               node_color='#ffcccc',
                               node_size=150, font_size=8)
        nx.draw_networkx_edges(self.__g, pos=pos, edgelist=self.__cutset,
                               edge_color='r', width=costs)
        plt.gca().set_axis_off()
        plt.gca().set_aspect('equal')
        plt.tight_layout()
        plt.savefig('multiway_e2.png', bbox_inches='tight')
        plt.show()


def gen(k=3):
    g = nx.LCF_graph(20, [1, 3, 14], 5)

    random.seed(3)
    srcs = random.sample(range(g.number_of_nodes()), k)

    for u, v in g.edges_iter():
        g[u][v]['cost'] = random.uniform(1, 3)

    return (g, srcs)


if __name__ == '__main__':
    g, srcs = gen()
    cs = multiway_cut(g, srcs)
    cs.draw()
