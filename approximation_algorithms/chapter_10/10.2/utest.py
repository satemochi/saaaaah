import random
import unittest
import networkx as nx
from tree import max_independent_set_for_tree


class test_independent_set_for_tree(unittest.TestCase):
    def test_independence(self):
        g, iset = self.__gen()
        self.assertTrue(self.__independence(g, iset))

    def __gen(self):
        g = nx.balanced_tree(3, 4)
        for v in g.nodes():
            g.node[v]['w'] = random.expovariate(1. / 50.0)
        return g, max_independent_set_for_tree(g).independent_set

    def __independence(self, g, iset):
        for i, v in enumerate(iset):
            if any(w in iset[i:] for w in g[v]):
                return False
        return True


if __name__ == '__main__':
    unittest.main()
