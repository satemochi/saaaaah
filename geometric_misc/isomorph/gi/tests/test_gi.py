import os
import random
import struct
import sys
import networkx as nx
from gi import is_isomorphic
from gi import vf2_iso, vf2_iso_simple


class TestWikipediaExample(object):
    # Source: https://en.wikipedia.org/wiki/Graph_isomorphism

    # Nodes 'a', 'b', 'c' and 'd' form a column.
    # Nodes 'g', 'h', 'i' and 'j' form a column.
    g1edges = [['a', 'g'], ['a', 'h'], ['a', 'i'],
               ['b', 'g'], ['b', 'h'], ['b', 'j'],
               ['c', 'g'], ['c', 'i'], ['c', 'j'],
               ['d', 'h'], ['d', 'i'], ['d', 'j']]

    # Nodes 1,2,3,4 form the clockwise corners of a large square.
    # Nodes 5,6,7,8 form the clockwise corners of a small square
    g2edges = [[1, 2], [2, 3], [3, 4], [4, 1],
               [5, 6], [6, 7], [7, 8], [8, 5],
               [1, 5], [2, 6], [3, 7], [4, 8]]

    def test_graph(self):
        g1, g2 = nx.Graph(self.g1edges), nx.Graph(self.g2edges)
        assert is_isomorphic(g1, g2)
        assert is_isomorphic(g1, g2, problem='sub')
        assert is_isomorphic(g1, g2, problem='mono')
        assert is_isomorphic(g1, g2, problem='homo')

    def test_mapping(self):
        g1, g2 = nx.Graph(self.g1edges), nx.Graph(self.g2edges)
        m1 = sorted(vf2_iso(g1, g2).mapping.items())
        m2 = sorted(vf2_iso_simple(g1, g2).mapping.items())
        isomap = [('a', 1), ('b', 6), ('c', 3), ('d', 8),
                  ('g', 2), ('h', 5), ('i', 4), ('j', 7)]
        assert all(m1[i] == isomap[i] for i in range(len(m1)))
        assert all(m2[i] == isomap[i] for i in range(len(m2)))

    def test_subgraph(self):
        g1, g2 = nx.Graph(self.g1edges), nx.Graph(self.g2edges)
        g3 = g2.subgraph([1, 2, 3, 4])
        assert is_isomorphic(g1, g3, problem='sub')

    def test_subgraph_mono(self):
        g1, g2 = nx.Graph(self.g1edges), nx.Graph([[1, 2], [2, 3], [3, 4]])
        assert is_isomorphic(g1, g2, problem='mono')


class TestVF2GraphDB(object):
    # http://amalfi.dis.unina.it/graph/db/

    @staticmethod
    def create_graph(fname):
        """Creates a Graph instance from the filename."""

        # The file is assumed to be in the format from the VF2 graph database.
        # Each file is composed of 16-bit numbers (unsigned short int).
        # So we will want to read 2 bytes at a time.

        # We can read the number as follows:
        #   number = struct.unpack('<H', file.read(2))
        # This says, expect the data in little-endian encoding
        # as an unsigned short int and unpack 2 bytes from the file.

        with open(fname, 'rb') as f:
            n = struct.unpack('<H', f.read(2))[0]
            g = nx.Graph()
            for u in range(n):
                m = struct.unpack('<H', f.read(2))[0]
                for e in range(m):
                    v = struct.unpack('<H', f.read(2))[0]
                    g.add_edge(u, v)
            return g

    def test_graph(self):
        head, tail = os.path.split(__file__)
        g1 = self.create_graph(os.path.join(head, 'iso_r01_s80.A99'))
        g2 = self.create_graph(os.path.join(head, 'iso_r01_s80.B99'))
        assert is_isomorphic(g1, g2)

    def test_subgraph(self):
        # A is the subgraph
        # B is the full graph
        head, tail = os.path.split(__file__)
        subgraph = self.create_graph(os.path.join(head, 'si2_b06_m200.A99'))
        graph = self.create_graph(os.path.join(head, 'si2_b06_m200.B99'))
        assert is_isomorphic(graph, subgraph, problem='sub')
        assert is_isomorphic(graph, subgraph, problem='mono')

    # There isn't a similar test implemented for subgraph monomorphism,
    # feel free to create one.


class TestAtlas(object):
    @classmethod
    def setup_class(cls):
        global atlas
        import platform
        if platform.python_implementation() == 'Jython':
            pytest.mark.skip('graph atlas not available under Jython.')
        import networkx.generators.atlas as atlas

        cls.GAG = atlas.graph_atlas_g()

    def test_graph_atlas(self):
        # Atlas = nx.graph_atlas_g()[0:208] # 208, 6 nodes or less
        Atlas = self.GAG[0:200]
        alphabet = list(range(26))
        for graph in Atlas:
            nlist = list(graph)
            labels = alphabet[:len(nlist)]
            for s in range(10):
                random.shuffle(labels)
                d = dict(zip(nlist, labels))
                relabel = nx.relabel_nodes(graph, d)
                if relabel.order() < 1:
                    continue
                assert is_isomorphic(graph, relabel)
                assert is_isomorphic(graph, relabel, problem='sub')
                assert is_isomorphic(graph, relabel, problem='mono')
                assert is_isomorphic(graph, relabel, problem='homo')


def test_multiedge():
    # Simple test for multigraphs
    # Need something much more rigorous
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
             (5, 6), (6, 7), (7, 8), (8, 9), (9, 10),
             (10, 11), (10, 11), (11, 12), (11, 12),
             (12, 13), (12, 13), (13, 14), (13, 14),
             (14, 15), (14, 15), (15, 16), (15, 16),
             (16, 17), (16, 17), (17, 18), (17, 18),
             (18, 19), (18, 19), (19, 0), (19, 0)]
    nodes = list(range(20))

    g1 = nx.MultiGraph()
    g1.add_edges_from(edges)
    for _ in range(10):
        new_nodes = list(nodes)
        random.shuffle(new_nodes)
        d = dict(zip(nodes, new_nodes))
        g2 = nx.relabel_nodes(g1, d)
        assert is_isomorphic(g1, g2)
        assert is_isomorphic(g1, g2, problem='sub')
        assert is_isomorphic(g1, g2, problem='mono')


def test_selfloop():
    # Simple test for graphs with selfloops
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 2),
             (2, 4), (3, 1), (3, 2), (4, 2), (4, 5), (5, 4)]
    nodes = list(range(6))

    g1 = nx.Graph(edges)
    for _ in range(100):
        new_nodes = list(nodes)
        random.shuffle(new_nodes)
        d = dict(zip(nodes, new_nodes))
        g2 = nx.relabel_nodes(g1, d)
        assert is_isomorphic(g1, g2)


def test_selfloop_mono():
    # Simple test for graphs with selfloops
    edges0 = [(0, 1), (0, 2), (1, 2), (1, 3),
             (2, 4), (3, 1), (3, 2), (4, 2), (4, 5), (5, 4)]
    edges = edges0 + [(2, 2)]
    nodes = list(range(6))

    g1 = nx.Graph(edges)
    for _ in range(100):
        new_nodes = list(nodes)
        random.shuffle(new_nodes)
        d = dict(zip(nodes, new_nodes))
        g2 = nx.relabel_nodes(g1, d)
        assert is_isomorphic(g1, g2, problem='mono')
        g2.remove_edges_from(nx.selfloop_edges(g2))
        assert is_isomorphic(g1, g2, problem='mono')


def test_isomorphism_iter2():
    # Path
    for L in range(2, 10):
        g1 = nx.path_graph(L)
        s = len(list(vf2_iso(g1, g1).iterate_isomorphisms()))
        assert s == 2
    # Cycle
    for L in range(3, 10):
        g1 = nx.cycle_graph(L)
        s = len(list(vf2_iso(g1, g1).iterate_isomorphisms()))
        assert s == 2 * L


def test_multiple():
    # Verify that we can use the graph matcher multiple times
    edges = [('A', 'B'), ('B', 'A'), ('B', 'C')]
    g1, g2 = nx.Graph(edges), nx.Graph(edges)
    g3 = nx.subgraph(g2, ['A', 'B'])
    assert is_isomorphic(g1, g2)
    g2.remove_node('C')
    assert is_isomorphic(g1, g2, problem='sub')
    assert is_isomorphic(g1, g3, problem='sub')
    assert is_isomorphic(g1, g2, problem='mono')
    assert is_isomorphic(g1, g3, problem='mono')
    assert is_isomorphic(g1, g2, problem='homo')
    assert is_isomorphic(g1, g3, problem='homo')


def test_noncomparable_nodes():
    node1 = object()
    node2 = object()
    node3 = object()

    # Graph
    G = nx.path_graph([node1, node2, node3])
    assert is_isomorphic(G, G)
    assert is_isomorphic(G, G, problem='mono')


def test_homomorphic():
    k4 = nx.complete_graph(4)   # is 4-colorable?
    for n in range(2, 9):
        g = nx.dorogovtsev_goltsev_mendes_graph(n)  # generate a planar graph
        assert is_isomorphic(g, k4, problem='homo')
