from lpsolve55 import lpsolve, IMPORTANT
from random_ksat import generate_instance
import random
import math


class maxsat:
    """ max sat problems """
    def __init__(self, nv, clauses, costs=None):
        self.__nc = len(clauses)
        self.__nv = nv
        self.__clauses = clauses
        self.__N = self.__nc + self.__nv
        self.__costs = costs if costs else [1] * self.__nc
        self.__lp = lpsolve('make_lp', 0, self.__N)

    def __len__(self):
        return self.__nv

    def __set_objective(self):
        lpsolve('set_maxim', self.__lp)
        lpsolve('set_obj_fn', self.__lp, self.__costs + [0] * self.__nv)

    def __set_constraints(self):
        for j, c in enumerate(self.__clauses):
            v = [0] * self.__N
            v[j] = 1
            d = 0
            for i in c:
                if i < 0:
                    v[self.__nc + abs(i) - 1] = 1
                    d += 1
                else:
                    v[self.__nc + i - 1] = -1
            lpsolve('add_constraint', self.__lp, v, 'LE', d)

    def __set_bounds(self):
        lpsolve('set_upbo', self.__lp, [1] * self.__N)
        lpsolve('set_lowbo', self.__lp, [0] * self.__N)

    def __config(self):
        lpsolve('set_verbose', self.__lp, IMPORTANT)
        lpsolve('write_lp', self.__lp, 'maxsat.lp')

    def __lp_setting(self):
        self.__set_objective()
        self.__set_constraints()
        self.__set_bounds()
        self.__config()

    def get(self):
        if lpsolve('get_Nrows', self.__lp) == 0:
            self.__lp_setting()
            lpsolve('solve', self.__lp)
        obj = lpsolve('get_objective', self.__lp)
        var = lpsolve('get_variables', self.__lp)[0][self.__nc:]
        return (obj, var)

    def o(self, signs):
        assert len(signs) == self.__nv, '[length error]'
        assert all(s in [-1, 1] for s in signs), '[value error]'
        costs = 0
        for i, c in enumerate(self.__clauses):
            for l in c:
                if l * signs[abs(l) - 1] > 0:
                    costs += self.__costs[i]
                    break
        return costs


def clauses(s):
    return [[int(v) for v in l.split(' ')[:-1]] for l in s.split('\n')[2:-1]]


def gen(nc=15, nv=10, k=5, op=False):
    return clauses(generate_instance(nc, nv, k, op))


def randomized_rounding(sat):
    o, v = sat.get()
    signs = [-1 if random.random() > v[i] else 1 for i in range(len(sat))]
    print 'randomized rounding:', signs
    return sat.o(signs)


if __name__ == '__main__':
    random.seed(0)
    c, v, k = 100, 10, 2
    cs = gen(c, v, k)
    costs = [random.random() for i in range(c)]

    sat = maxsat(v, cs, costs)
    print randomized_rounding(sat)
