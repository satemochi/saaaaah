from random import getrandbits
from matplotlib import pyplot as plt
import networkx as nx
from k_regular_hyper_graph import random_k_regular_hyper_graph, draw


class kcnf:
    def __init__(self, n, d):
        self.hg = random_k_regular_hyper_graph(n, d)
        self.edges = list(self.hg.keys())
        self.nodes = list(range(min(self.edges)))
        self.negates = {e: [((b := getrandbits(d)) >> i) & 1 for i in range(d)]
                        for e in self.edges}
        print(self.edges)
        print(self.nodes)
        from pprint import pprint
        pprint(self.hg)
        pprint(self.negates)

    def __verify_truth_assignments(self, a):
        assert(len(a) == len(self.nodes))
        assert(all(v in (0, 1) for v in a))
        return all(any(a[v] * self.negates[e][i] > 0 for i, v in iv)
                    for e, iv in self.hg.items())

    def __return_truth_assignments(self):
        pass
    

if __name__ == '__main__':
    print('hello')
#    g = random_k_regular_hyper_graph(20, 3)
#    draw(g)
#    plt.show()
    kcnf(10, 3)
