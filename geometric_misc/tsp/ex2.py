from time import time
from matplotlib import pyplot as plt
import numpy as np
from tsp import ordinary_mtz, enhanced_mtz, lazy_generation, lazy_generation2

def eval(solver, pts):
    start = time()
    solver(pts)
    return time() - start

def e(trials=10, seed=1):
    np.random.seed(seed)
#    sizes = list(range(5, 31))
#    sizes = list(range(5, 20))
#    sizes = list(range(5, 10))
#    sizes = list(range(30, 50))
#    sizes = list(range(20, 30))
    sizes = list(range(100, 150))
    to, te = [], []
    Po, Pe = [], []
    for n in sizes:
        print(n)
        tto, tte = 0, 0
        po, pe = [], []
        for i in range(trials):
            P = np.random.random((n, 2))
#            tto += eval(ordinary_mtz, P)
#            tte += eval(enhanced_mtz, P)
            t1 = eval(lazy_generation, P)
            t2 = eval(lazy_generation2, P)
            tto += t1
            tte += t2
            po.append(t1)
            pe.append(t2)
        to.append(tto / trials)
        te.append(tte / trials)
        Po.append(po)
        Pe.append(pe)

#    plt.plot(sizes, to, label='ordinary', marker='o')
#    plt.plot(sizes, te, label='enhanced', marker='o')
    plt.plot(sizes, to, label='lazy 1', marker='o')
    plt.plot(sizes, te, label='lazy 2', marker='o')
    for i, n in enumerate(sizes):
#        plt.scatter([n] * trials, Po[i], marker='x', c='g')
#        plt.scatter([n] * trials, Pe[i], marker='x', c='r')
        plt.boxplot(Po[i], positions=[n-0.10])
        plt.boxplot(Pe[i], positions=[n+0.10])
    plt.xticks(sizes, sizes)

    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('experiment15.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    e()
