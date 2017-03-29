from lpsolve55 import lpsolve, IMPORTANT
from random_ksat import generate_instance
import random


class maxsat:
    """ max sat problems """
    def __init__(self, nv, clauses, costs=None):
        self.__nv = nv
        self.__clauses = clauses
        self.__costs = costs if costs else [1] * len(clauses)

    def __len__(self):
        return self.__nv

    def o(self, signs):
        assert len(signs) == self.__nv, '[length error]'
        assert sum([abs(i) for i in signs]) == self.__nv, '[value error]'
        costs = 0
        for c in self.__clauses:
            for l in c:
                if l * signs[abs(l) - 1] > 0:
                    costs += self.__costs[abs(l) - 1]
                    break
        return costs


def clauses(s):
    return [[int(v) for v in l.split(' ')[:-1]] for l in s.split('\n')[2:-1]]


def gen(nc=15, nv=10, k=5, op=False):
    return clauses(generate_instance(nc, nv, k, op))


def simple_algorithm(sat):
    return [random.choice([1, -1]) for i in range(len(sat))]


if __name__ == '__main__':
    random.seed(0)
    c, v, k = 100, 30, 2
    cs = gen(c, v, k)
    costs = [random.random() for i in range(c)]

    sat = maxsat(v, cs, costs)
    print sat.o(simple_algorithm(sat))
