from scpgen import scpgen
import sys
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS
import numpy as np
from lpsolve55 import lpsolve, IMPORTANT


def greedy(scp_gen):
    n, m = scp_gen.universal_set_size, scp_gen.covering_set_num
    S = set([])     # for checking whether the universal set is covered
    H = [set(scp_gen.sets[j]) for j in range(m)]
    I = [0] * m
    while len(S) != n:
        ell = np.argmin([float(scp_gen.cost[j]) / len(H[j])
                         if len(H[j]) else sys.maxint for j in range(m)])
        I[ell] = 1
        S |= H[ell]
        for j in range(m):
            if not len(H[j]) or j == ell:
                continue
            H[j] -= H[ell]
        H[ell] = set([])
    return I


def draw(sc, I=None, ax=None):
    n, m = sc.universal_set_size, sc.covering_set_num
    if I is None:
        I = [1] * m
    if ax is None:
        ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(color="#cccccc")
    cnames = CSS4_COLORS.values()[59:]
    for y, val in enumerate(I):
        if val == 0:
            continue
        c = cnames[y]
        for e in range(sc.sizes[y]):
            x = sc.sets[y][e]
            rect = plt.Rectangle((x-0.5, y-0.5), 1, 1, alpha=0.75, color=c)
            ax.add_patch(rect)

if __name__ == '__main__':
    sc = scpgen(10, 20, 0.5, 0)
    f, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True,
                                 figsize=(13, 3))
    n, m = sc.universal_set_size, sc.covering_set_num
    plt.xlim([-0.5, n - 0.5])
    plt.ylim([-0.5, m - 0.5])
    plt.xticks(range(n), range(n))
    plt.yticks(range(m), range(m))

    draw(sc, ax=ax1)
    ans = greedy(sc)
    draw(sc, I=ans, ax=ax2)

    plt.title('greedy algorithm')
    plt.tight_layout()
    plt.savefig('setcover_greedy_example.png', bbox_inches='tight')
    plt.show()
