import os.path
import pickle
from itertools import product, combinations
from lpsolve55 import lpsolve, IMPORTANT
import networkx as nx


class programming_for_tree_decomposition:
    def __init__(self, g, is_force=False):
        self.g = g
        self.n = g.number_of_nodes()
        self.N = self.n * self.n
        self.zeros = [0] * (2 * self.N)

        if not is_force and os.path.exists('vars.pickle'):
            with open('vars.pickle', 'rb') as f:
                self.vars = pickle.load(f)
        else:
            self.lp = lpsolve('make_lp', 0, 2 * self.N)
            lpsolve('set_obj_fn', self.lp, [1] + [0] * (2 * self.N - 1))
            lpsolve('set_binary', self.lp, [0] + [1] * (2 * self.N - 1))
            lpsolve('set_verbose', self.lp, IMPORTANT)
            self.__add_constraints()
            lpsolve('write_lp', self.lp, 'a.lp')
            lpsolve('solve', self.lp)
            self.vars = lpsolve('get_variables', self.lp)[0]
            with open('vars.pickle', 'wb') as f:
                pickle.dump(self.vars, f)

    def __add_constraints(self):
        self.__determine_max_clique_size()
        self.__total_order()
        self.__transitivity()
        self.__gearing_xy()
        self.__counting_edges()
        self.__counting_chord()

    def __determine_max_clique_size(self):   # 2
        T, x, y = self.zeros, self.__x, self.__y
        T[0] = 1
        for i in self.g.nodes():
            for j in self.g.nodes():
                if i == j:
                    continue
                T[y(i, j)] = -1
            lpsolve('add_constraint', self.lp, T, 'GE', 0)
            for j in self.g.nodes():
                if i == j:
                    continue
                T[y(i, j)] = 0
            assert(T.count(1) == 1)
        T[0] = 0
        assert(self.zeros.count(1) == 0)

    def __x(self, i, j):
        assert(i != j)
        return self.n * i + j

    def __y(self, i, j):
        return self.N + self.__x(i, j)

    def __total_order(self):                  # 3
        T, x, y = self.zeros, self.__x, self.__y
        for i, j in product(self.g.nodes(), repeat=2):
            if i == j:
                continue
            T[x(i, j)] = 1
            T[x(j, i)] = 1
            lpsolve('add_constraint', self.lp, T, 'EQ', 1)
            T[x(i, j)], T[x(j, i)] = 0, 0

    def __transitivity(self):                 # 4
        T, x, y = self.zeros, self.__x, self.__y
        for i, j, k in product(self.g.nodes(), repeat=3):
            if i == j or j == k or i == k:
                continue
            T[x(i, j)] = 1
            T[x(j, k)] = 1
            T[x(i, k)] = -1
            lpsolve('add_constraint', self.lp, T, 'LE', 1)
            T[x(i, j)], T[x(j, k)], T[x(i, k)] = 0, 0, 0

    def __gearing_xy(self):                       # 5
        T, x, y = self.zeros, self.__x, self.__y
        for i, j in product(self.g.nodes(), repeat=2):
            if i == j:
                continue
            T[x(i, j)] = -1
            T[y(i, j)] = 1
            lpsolve('add_constraint', self.lp, T, 'LE', 0)
            T[x(i, j)], T[y(i, j)] = 0, 0

    def __counting_edges(self):     # 6
        T, x, y = self.zeros, self.__x, self.__y
        for i, j in self.g.edges():
            T[x(i, j)] = -1
            T[y(i, j)] = 1
            lpsolve('add_constraint', self.lp, T, 'EQ', 0)
            T[x(i, j)], T[y(i, j)] = 0, 0

            T[x(j, i)] = -1
            T[y(j, i)] = 1
            lpsolve('add_constraint', self.lp, T, 'EQ', 0)
            T[x(j, i)], T[y(j, i)] = 0, 0

    def __counting_chord(self):      # 7
        T, x, y = self.zeros, self.__x, self.__y
        for i, j, k in product(self.g.nodes(), repeat=3):
            if i == j or j == k or i == k:
                continue
            T[x(j, k)] = 1
            T[y(i, j)] = 1
            T[y(i, k)] = 1
            T[y(j, k)] = -1
            lpsolve('add_constraint', self.lp, T, 'LE', 2)
            T[x(j, k)], T[y(i, j)], T[y(i, k)], T[y(j, k)] = 0, 0, 0, 0

    def tree_decomposition(self):
        t = nx.Graph()
        tbc = []    # to be connected
        for v in self.__elimination_ordering():
            c = self.__partial_clique(v)
            for cc in tbc:
                if set(c) <= set(cc):   # whether c is contained in cc
                    c = cc
                    break
            for cc in tbc:
                if v in cc:
                    if c != cc:
                        t.add_edge(tuple(c), tuple(cc))
            tbc = [x for x in tbc if v not in x] + [c]
        for v in t.nodes():
            t.node[v]['label'] = str(v)
        return t

    def __elimination_ordering(self):
        order = [0] * self.n
        for v in self.g.nodes():
            order[self.__rank_of(v)] = v
        return order

    def __rank_of(self, i):
        vs = self.vars[self.n * i: self.n * i + self.n]
        return self.n - vs.count(1.0) - 1

    def __partial_clique(self, u):
        begin, end = self.N + self.n * u, self.N + self.n * (u + 1)
        c = [u]
        for v, x in enumerate(self.vars[begin: end]):
            if x > 0:
                c.append(v)
        return c

    @property
    def tree_width(self):
        return self.vars[0]
