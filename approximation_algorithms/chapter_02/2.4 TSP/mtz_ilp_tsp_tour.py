import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from itertools import product
from lpsolve55 import lpsolve, IMPORTANT, Infinite


def incomming_constraints(n):
    N = n**2
    for j in range(n):
        const_vector = [0] * (N + n)
        for i in range(n):
            if i == j:
                continue
            const_vector[n * i + j] = 1
        yield const_vector


def outgoing_constraints(n):
    N = n**2
    for i in range(n):
        const_vector = [0] * (N + n)
        for j in range(n):
            if i == j:
                continue
            const_vector[n * i + j] = 1
        yield const_vector


def subtour_constraints(n):
    N = n**2
    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                continue
            const_vector = [0] * (N + n)
            const_vector[n * i + j] = n
            const_vector[N + i] = 1
            const_vector[N + j] = -1
            yield const_vector


def set_bounds(lp, N, n):
    lpsolve('set_int', lp, [1] * (N + n))
    lpsolve('set_upbo', lp, [1] * N + [n-1] * n)
    lpsolve('set_lowbo', lp, [0] * N + [1] * n)
    lpsolve('set_upbo', lp, N + 1, 0)
    lpsolve('set_lowbo', lp, N + 1, 0)


def set_constraints(lp, n):
    for v in incomming_constraints(n):
        lpsolve('add_constraint', lp, v, 'EQ', 1)
    for v in outgoing_constraints(n):
        lpsolve('add_constraint', lp, v, 'EQ', 1)
    for v in subtour_constraints(n):
        lpsolve('add_constraint', lp, v, 'LE', n - 1)


def config_lp(lp):
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('write_lp', lp, 'mtz_ilp_formulae.lp')


def get_mtz_ilp_tour(P):
    n, N = len(P), len(P)**2
    d = [np.linalg.norm(P[i] - P[j]) for i, j in product(range(n), range(n))]

    lp = lpsolve('make_lp', 0, N + n)
    lpsolve('set_obj_fn', lp, d + [0] * len(P))
    set_constraints(lp, n)
    set_bounds(lp, N, n)
    config_lp(lp)

    lpsolve('solve', lp)

    tour = [0] * (n + 1)
    for i, v in enumerate(lpsolve('get_variables', lp)[0][N:]):
        tour[int(v)] = i
    return tour


def draw_tour(P, tour):
    plt.scatter(P[:, 0], P[:, 1])

    lines = [[P[i], P[j]] for i, j in zip(tour[:-1], tour[1:])]
    plt.gca().add_collection(mc.LineCollection(lines, colors='g',
                                               linewidth=2, zorder=-1))

if __name__ == '__main__':
    P = np.random.random((10, 2))
    draw_tour(P, get_mtz_ilp_tour(P))
    plt.show()
