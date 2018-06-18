import unittest
import networkx as nx
from tree_decomp import programming_for_tree_decomposition


class test_tree_decomp(unittest.TestCase):
    g, t = None, None

    @classmethod
    def setUpClass(cls):
        cls.g = nx.petersen_graph()
        a = programming_for_tree_decomposition(cls.g, True)
        cls.t = a.tree_decomposition()

    def test_vertex_cover(self):
        bags = set([])
        for b in self.t.nodes():
            bags |= set(b)
        self.assertEqual(bags, set(self.g.nodes()))

    def test_edge_cover(self):
        self.assertTrue(self.__test_edge_cover())

    def __test_edge_cover(self):
        for e in self.g.edges():
            if not any(set(e) <= set(bag) for bag in self.t.nodes()):
                return False
        return True

    def test_subtree(self):
        self.assertTrue(self.__test_subtree())

    def __test_subtree(self):
        for v in self.g.nodes():
            nl = [w for w in self.t.nodes() if v in w]
            sub_g = self.t.subgraph(nl)
            if not nx.is_connected(sub_g):
                return False
        return True


if __name__ == '__main__':
    unittest.main()
