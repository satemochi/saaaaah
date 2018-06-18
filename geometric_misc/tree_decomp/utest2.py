import unittest
import networkx as nx
from tree_decomp import programming_for_tree_decomposition


class test_jobs(unittest.TestCase):
    g, t = None, None

    def test_house_graph(self):
        print '\nhouse:',
        self.g = nx.house_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    def __test_all_conditions(self):
        return (self.__vertex_cover() and self.__edge_cover()
                and self.__subtree())

    def __vertex_cover(self):
        bags = set([])
        for b in self.t.nodes():
            bags |= set(b)
        return bags == set(self.g.nodes())

    def __edge_cover(self):
        for e in self.g.edges():
            if not any(set(e) <= set(bag) for bag in self.t.nodes()):
                return False
        return True

    def __subtree(self):
        for v in self.g.nodes():
            nl = [w for w in self.t.nodes() if v in w]
            sub_g = self.t.subgraph(nl)
            if not nx.is_connected(sub_g):
                return False
        return True

    def test_bull(self):
        print '\nbull:',
        self.g = nx.bull_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    @unittest.skip('too much time to create instance...')
    def test_chvatal(self):
        print '\nchvatal:',
        self.g = nx.chvatal_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    def test_cubical(self):
        print '\ncubical:',
        self.g = nx.cubical_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    @unittest.skip('too much time to create instance...')
    def test_desargues(self):
        print '\ndesargues:',
        self.g = nx.desargues_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    def test_diamond(self):
        print '\ndiamond:',
        self.g = nx.diamond_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    @unittest.skip('too much time to create instance...')
    def test_dodecahedral(self):
        print '\ndodecahedral:',
        self.g = nx.dodecahedral_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    @unittest.skip('too much time to create instance...')
    def test_frucht(self):
        print '\nfrucht:',
        self.g = nx.frucht_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())

    @unittest.skip('too much time to create instance...')
    def test_petersen(self):
        print '\npetersen:',
        self.g = nx.petersen_graph()
        a = programming_for_tree_decomposition(self.g, True)
        self.t = a.tree_decomposition()
        self.assertTrue(self.__test_all_conditions())


if __name__ == '__main__':
    unittest.main()
