from lpsolve55 import lpsolve, IMPORTANT


class max_independent_set_with_ILP:
    def __init__(self, g):
        self.g = g
        self.n = g.number_of_nodes()
        self.zeros = [0] * self.n
        self.__lp()
        self.__independent_set()

    def __lp(self):
        self.lp = lpsolve('make_lp', 0, self.n)
        lpsolve('set_maxim', self.lp)
        weights = [self.g.node[v]['w'] for v in self.g.nodes()]
        lpsolve('set_obj_fn', self.lp, weights)
        lpsolve('set_binary', self.lp, [1] * self.n)
        lpsolve('set_verbose', self.lp, IMPORTANT)
        self.__add_constraints()
        lpsolve('write_lp', self.lp, 'b.lp')
        lpsolve('solve', self.lp)

    def __add_constraints(self):
        T = self.zeros
        for u, v in self.g.edges():
            T[u], T[v] = 1, 1
            lpsolve('add_constraint', self.lp, T, 'LE', 1)
            T[u], T[v] = 0, 0

    def __independent_set(self):
        self.__is = []
        for i, x in enumerate(lpsolve('get_variables', self.lp)[0]):
            if x > 0:
                self.__is.append(i)

    @property
    def independent_set(self):
        return self.__is
