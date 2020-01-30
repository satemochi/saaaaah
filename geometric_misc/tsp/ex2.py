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
    sizes = list(range(5, 20))
    to, te = [], []
    for n in sizes:
        print(n)
        tto, tte = 0, 0
        for i in range(trials):
            P = np.random.random((n, 2))
            tto += eval(ordinary_mtz, P)
            tte += eval(enhanced_mtz, P)
#            tto += eval(lazy_generation, P)
#            tte += eval(lazy_generation2, P)
        to.append(tto / trials)
        te.append(tte / trials)

    plt.plot(sizes, to, label='ordinary', marker='o')
    plt.plot(sizes, te, label='enhanced', marker='o')
#    plt.plot(sizes, to, label='lazy 1', marker='o')
#    plt.plot(sizes, te, label='lazy 2', marker='o')

    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('experiment11.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    e()
