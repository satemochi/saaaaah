from fractions import Fraction
import itertools
from lpsolve55 import lpsolve, IMPORTANT
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class item:
    def __init__(self, n, numerator, denominator):
        self.n = n
        self.size = Fraction(numerator, denominator)


class pattern:
    def __init__(self, items):
        self.pat = []
        self.items = items
        max_denom = max([i.size.denominator for i in items])
        for v in itertools.product(range(max_denom+1), repeat=len(items)):
            size = 0
            for i in range(len(items)):
                size += v[i] * float(items[i].size)
            if size <= 1:
                self.pat.append(v)
        del self.pat[0]
        print len(self.pat)

    def gen(self):
        for i in range(len(self.pat[0])):
            yield ([p[i] for p in self.pat], self.items[i].n)


def get_instance():
    items = [item(9, 1, 5), item(7, 1, 4), item(4, 1, 8), item(3, 1, 6),
             item(2, 1, 7)]
    for i in range(len(items)):
        print items[i].size, items[i].n
    return items


def comp_lp(pat):
    lp = lpsolve('make_lp', 0, len(pat.pat))
    lpsolve('set_verbose', lp, IMPORTANT)
#    lpsolve('set_binary', lp, range(len(pat.pat)))
    lpsolve('set_int', lp, range(len(pat.pat)))
    lpsolve('set_obj_fn', lp, [1] * len(pat.pat))
    for p, n in pat.gen():
        lpsolve('add_constraint', lp, p, 'EQ', n)
    lpsolve('solve', lp)
    print
    print lpsolve('get_objective', lp)
    variables = lpsolve('get_variables', lp)[0]
    V = []
    for i, v in enumerate(variables):
        if v == 0.0:
            continue
        print pat.pat[i], int(v)
        for x in range(int(v)):
            V.append(list(pat.pat[i]))
    return V


def get_next(L, items):
    while True:
        rval = []
        for l in L:
            if l == [0] * len(l):
                rval.append(0)
            else:
                for i in range(len(l)):
                    if l[i] == 0:
                        continue
                    l[i] -= 1
                    rval.append(float(items[i].size))
                    break
        if rval == [0] * len(L):
            raise StopIteration
        yield rval


def draw(L):
    X = range(len(L))
    Y = []
    for v in get_next(L, items):
        Y.append(v)

    offset = [0] * len(Y[0])
    plt.bar(X, Y[0], align='center', color=cm.hot(map(lambda c: c*2.5, Y[0])))
    for p in zip(range(1, len(Y)), range(0, len(Y)-1)):
        offset = [a + b for a, b in zip(Y[p[1]], offset)]
        plt.bar(X, Y[p[0]], bottom=offset, align='center',
                color=cm.hot(map(lambda c: c*2.5, Y[p[0]])))
#    plt.savefig('bin_packing02.png', bbox_inches='tight')
    plt.gca().margins(0.1)
    plt.show()

if __name__ == '__main__':
    items = get_instance()
    pat = pattern(items)
    draw(comp_lp(pat))
