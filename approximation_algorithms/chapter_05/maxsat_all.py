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
                    v[self.__nc - 1 + abs(i)] = 1
                    d += 1
                else:
                    v[self.__nc - 1 + i] = -1
            lpsolve('add_constraint', self.__lp, v, 'LE', d)

    def __set_bin(self, flag=True):
        if flag:
            lpsolve('set_binary', self.__lp, [0] * self.__nc + [1] * self.__nv)
        else:
            lpsolve('set_binary', self.__lp, [0] * self.__N)

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

    def __get(self, bin=True):
        if lpsolve('get_Nrows', self.__lp) == 0:
            self.__lp_setting()
            self.__set_bin(bin)
            lpsolve('solve', self.__lp)
        elif bin and lpsolve('is_binary', self.__lp, self.__N) == 0:
            self.__set_bin(bin)
            lpsolve('solve', self.__lp)
        elif not bin and lpsolve('is_binary', self.__lp, self.__N) == 1:
            self.__set_bin(bin)
            lpsolve('solve', self.__lp)

        obj = lpsolve('get_objective', self.__lp)
        var = lpsolve('get_variables', self.__lp)[0][self.__nc:]
        return (obj, var)

    def get(self, type='int'):
        if type in ['i', 'int']:
            return self.__get(True)
        elif type in ['f', 'float']:
            return self.__get(False)
        else:
            return (0.0, [])

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

    def e(self, signs):
        """ [signs] is a sequence consisting of {1, -1, 0, 1}^nc.
            '1' and '-1' imply True and False, respectively.
            '0' is unspecified but will be True with probability 1/2.
        """
        assert len(signs) == self.__nv, '[length error]'
        assert all(s in [-1, 0, 1] for s in signs), '[value error]'
        costs = 0
        for i, c in enumerate(self.__clauses):
            unknown = 0
            for l in c:
                if signs[abs(l) - 1] == 0:
                    unknown += 1
                elif l * signs[abs(l) - 1] > 0:
                    costs += self.__costs[i]
                    unknown = 0
                    break
            costs += self.__costs[i] * (1 - 0.5**unknown)
        return costs


def clauses(s):
    return [[int(v) for v in l.split(' ')[:-1]] for l in s.split('\n')[2:-1]]


def gen(nc=15, nv=10, k=5, op=False):
    return clauses(generate_instance(nc, nv, k, op))


def simple_algorithm(sat):
    signs = [random.choice([1, -1]) for i in range(len(sat))]
    print 'simple:', signs
    return sat.o(signs)


def derandomized_simple_algorithm(sat):
    signs = [0] * len(sat)  # init: all unknown or unspecified
    for i in range(len(sat)):
        signs[i] = 1
        t_ce = sat.e(signs) # the conditional expectation of being xi True
        signs[i] = -1
        f_ce = sat.e(signs)
        if t_ce > f_ce:     # choosing greather assignment.
            signs[i] = 1
    print 'derandomized:', signs
    return sat.o(signs)


def biased_coins(sat):
    p = 0.5 * (math.sqrt(5) - 1)
    signs = [-1 if random.random() > p else 1 for i in range(len(sat))]
    print 'biased coins:', signs
    return sat.o(signs)


def randomized_rounding(sat):
    o, v = sat.get('float')
    signs = [-1 if random.random() > v[i] else 1 for i in range(len(sat))]
    print 'randomized rounding:', signs
    return sat.o(signs)


def better_of_two(sat):
    simple = [random.choice([1, -1]) for i in range(len(sat))]
    o, v = sat.get('float')
    rr = [-1 if random.random() > v[i] else 1 for i in range(len(sat))]
    signs = simple if sat.o(simple) > sat.o(rr) else rr
    print 'better of two:', signs
    return sat.o(signs)


def nonlinear_prob(x):
    assert x >= 0 and x <= 1
    prob = random.uniform(1 - (0.25**x), 4**(x - 1))
    return random.random() <= prob


def nonlinear_randomized_rounding(sat):
    o, var = sat.get('float')
    signs = [1 if nonlinear_prob(v) else -1 for v in var]
    print 'nonlinear randomized rounding:', signs
    return sat.o(signs)

if __name__ == '__main__':
    random.seed(0)
    c, v, k = 100, 30, 2
    cs = gen(c, v, k)
    costs = [random.random() for i in range(c)]

    sat = maxsat(v, cs, costs)

    o, variables = sat.get()
    print 'integer programs:', [1 if v > 0 else -1 for v in variables]
    print o

    print simple_algorithm(sat)
    print derandomized_simple_algorithm(sat)
    print biased_coins(sat)
    print randomized_rounding(sat)
    print nonlinear_randomized_rounding(sat)
