from itertools import product
from time import time
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def mohapatra(a, b):
    n, dom = min(a.shape), list(range(a.shape))
    m = int(np.math.log10(max(a.max(), b.max()))) + 1
    p = int(np.math.log10((10**(2*m)-1)*n)) + 1
    pad1, pad2 = 10**p, 10**(p*(n-1))

    c = [int(sum(a[i,j]*(pad2//(pad1**j)) for j in dom)) for i in dom]
    d = [int(sum(b[-i-1,j]*(pad2//(pad1**i)) for i in dom)) for j in dom]
    e = np.zeros((n, n))
    for i, j in product(dom, repeat=2):
        e[i,j] = int(c[i]*d[j]//pad2) % pad1
    return e


def school(a, b):
    n = min(a.shape)
    c = np.zeros((n, n))
    for i, j, k in product(range(n), repeat=3):
        c[i,j] += a[i,k] * b[k,j]
    return c


def _test2():
    trials, num_of_nodes = 10, [10, 20, 30, 40, 50, 60, 70]
    tm, ti = [0] * len(num_of_nodes), [0] * len(num_of_nodes)
    for i, n in enumerate(num_of_nodes):
        print(n)
        for k in range(trials):
            a = nx.to_numpy_matrix(nx.fast_gnp_random_graph(n, 5/n))
            s = time()
            mohapatra(a, a)
            e = time()
            school(a, a)
            ti[i] += time() - e
            tm[i] += e - s
        tm[i] /= trials
        ti[i] /= trials

    plt.plot(num_of_nodes, tm, label='mohapatra', marker='o')
    plt.plot(num_of_nodes, ti, label='school algorithm', marker='o')
    plt.legend(loc='best')
    plt.xlabel('nxn matrix')
    plt.ylabel('elapsed time (seconds)')
    plt.tight_layout()
    plt.savefig('mohapatra_emprical_study_01.png', bbox_inches='tight')


if __name__ == '__main__':
    _test2()
