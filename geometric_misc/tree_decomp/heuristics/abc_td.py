from abc import ABCMeta, abstractmethod
from itertools import combinations
from random import choice
from matplotlib import pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


class abc_td:
    """ An abstract basic class for heuristics based on an elimination
        ordering which compute tree decompositions. Heuristics depicted
        in this file can be referred to the following literature;

        T. Hammerl, N. Musliu, and W. Schafhauser. (2015).
            Metaheuristic Algorithms and Tree Decomposition.
                In Handbook of Computational Intelligence,
                    pp. 1255-1270. Springer.
    """
    __metaclass__ = ABCMeta

    def _build(self, g, param=None):
        self.g = g.copy()   # because whole graph is deleted by _tree_decomp()
        self._ordering(param)
        self._tree_decomp()
        self._tree_width()
        if __debug__:
            self._test()

    @abstractmethod
    def _ordering(self, param=None):
        raise NotImplemented()

    def _tree_decomp(self):
        self._td = nx.Graph()
        tbc = []    # to be connected
        if __debug__:
            h = self.g.copy()
        for v in self._eo:
            c = self._partial_clique(v)
            for cc in tbc:
                if set(c) <= set(cc):   # whether c is fully contained by cc
                    c = cc
                    if not tuple(cc) in self.g:
                        self._td.add_node(tuple(cc))    # for complete graphs
                    break
            for cc in tbc:
                if v in cc and c != cc:
                    self._td.add_edge(tuple(c), tuple(cc))
            tbc = [x for x in tbc if v not in x] + [c]
        for v in self._td.nodes():
            self._td.node[v]['label'] = str(v)
        if __debug__:
            self.g = h

    def _partial_clique(self, u):
        c = [u] + list(self.g[u])
        self._make_simplicial(u)
        self.g.remove_node(u)
        return c

    def _make_simplicial(self, u):
        for i, j in combinations(self.g[u], 2):
            if not self.g.has_edge(i, j):
                self.g.add_edge(i, j)

    def _tree_width(self):
        self._tw = max(len(v) for v in self._td) - 1

    def _test(self):
        self._vcover()
        self._ecover()
        self._connectivity()

    def _vcover(self):
        bags = set([])
        for b in self._td.nodes():
            bags |= set(b)
        if bags != set(self.g.nodes()):
            raise UserWarning

    def _ecover(self):
        for e in self.g.edges():
            if not any(set(e) <= set(bag) for bag in self._td.nodes()):
                raise UserWarning

    def _connectivity(self):
        for v in self.g.nodes():
            nl = [w for w in self._td.nodes() if v in w]
            sub_g = self._td.subgraph(nl)
            if not nx.is_connected(sub_g):
                raise UserWarning

    @property
    def tree_decomposition(self):
        return self._td

    @property
    def elimination_ordering(self):
        return self._eo

    @property
    def tree_width(self):
        return self._tw

    def draw(self, ax):
        pos = graphviz_layout(self._td, prog='twopi', args='')
        nx.draw(self._td, pos, ax=ax, node_size=100, alpha=0.5, node_color='g')
        L = nx.get_node_attributes(self._td, 'label')
        nx.draw_networkx_labels(self._td, pos, ax=ax, font_size=8, labels=L)
        ax.margins(0.2)     # to restrict label-cut-off


class maximum_cardinality_search(abc_td):
    """ Maximum Cardinality Search (MCS) initially selects a random vertex of
        the graph to be the first vertex in the elimination ordering
        (the elimination ordering is constructed from right to left).
        The next vertex will be picked such that it has the highest
        connectivity with the vertices previously selected in
        the elimination ordering. Ties are broken randomly.  MCS repeats this
        process iteratively until all vertices are selected.
    """
    def __init__(self, g, first_vertex=None):
        self._build(g, first_vertex)

    def _ordering(self, first=None):
        self._eo = self.__init_eo(first)
        while len(self._eo) != self.g.number_of_nodes():
            self._eo = [self.__max_card()] + self._eo

    def __init_eo(self, first):
        if first and first in self.g:
            return [first]
        return self.__random_selection()

    def __random_selection(self):
        return [choice(list(self.g.nodes()))]

    def __max_card(self):
        return max([(self.__count_card(v), v) for v in self.g])[1]

    def __count_card(self, v):
        return 0 if v in self._eo else len(set(self._eo) & set(self.g[v]))


class min_fill(abc_td):
    """ The min-fill heuristic first picks the vertex which adds the smallest
        number of edges when eliminated (ties are broken randomly).
        The selected vertex is made simplicial (a vertex of a graph is
        simplicial if its neighbours form a clique) and it is eliminated from
        the graph. The next vertex in the ordering will be any vertex that
        adds the minimum number of edges when eliminated from the graph.
        This process is repeated iteratively until the whole elimination
        ordering is constructed.
    """
    def __init__(self, g):
        self._build(g)

    def _ordering(self, first=None):
        h = self.g.copy()
        self._eo = []
        while len(self._eo) != h.number_of_nodes():
            v = self.__min_fill()
            self._eo.append(v)
            self._partial_clique(v)
        self.g = h

    def __min_fill(self):
        return min([(self.__count_fill(v), v) for v in self.g])[1]

    def __count_fill(self, u):
        n_chord = 0
        for e in combinations(self.g[u], 2):
            if not self.g.has_edge(*e):
                n_chord += 1
        return n_chord


class min_degree(abc_td):
    """ The minimum degree heuristic picks first the vertex with the minimum
        degree. The selected vertex is made simplicial and it is removed
        from the graph. Further, the vertex that has the minimum number of
        unselected neighbours will be chosen as the next node in
        the elimination ordering. This process is repeated iteratively.
    """
    def __init__(self, g):
        self._build(g)

    def _ordering(self, first=None):
        h = self.g.copy()
        self._eo = []
        while len(self._eo) != h.number_of_nodes():
            v = self.__min_degree()
            self._eo.append(v)
            self._partial_clique(v)
        self.g = h

    def __min_degree(self):
        return min(list(self.g.degree()), key=lambda t: t[1])[0]


def draw(g, trees, titles, name):
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

    nx.draw(g, ax=ax1, with_labels=True)
    ax1.set_title(name)
    for ax, tree, title in zip((ax2, ax3, ax4), trees, titles):
        tree.draw(ax)
        ax.set_title(title)
    plt.savefig(name+'_tree_decomp.png', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    h_names = ['Max cardinality search', 'Min-fill', 'Min-degree']
    targets = {'bull': nx.bull_graph(),             # 1-connected planar
               'chvatal': nx.chvatal_graph(),       # 4-connected non-planar
               'cubical': nx.cubical_graph(),       # 3-connected planar
               'desargues': nx.desargues_graph(),   # 3-connected non-planar
               'diamond': nx.diamond_graph(),       # 2-connected planar
               'dodecahedral': nx.dodecahedral_graph(), # 3-connected planar
               'frucht': nx.frucht_graph(),         # 3-connected planar
               'heawood': nx.heawood_graph(),       # 3-connected planar
               'house': nx.house_graph(),           # 2-connected planar
               'house_x': nx.house_x_graph(),       # 2-connected planar
               'icosahedral': nx.icosahedral_graph(),   # 5-connected planar
               'krackhardt': nx.krackhardt_kite_graph(),# 1-connected planar
               'moebius': nx.moebius_kantor_graph(),    # non-planar
               'octahedral': nx.octahedral_graph(),     # 4-connected planar
               'pappus': nx.pappus_graph(),         # 3-connected non-planar
               'petersen': nx.petersen_graph(),     # 3-connected non-planar
               'sedgewick': nx.sedgewick_maze_graph(),  # 1-connected planar
               'tetrahedral': nx.tetrahedral_graph(),   # 3-connected planar
               'truncated_cube': nx.truncated_cube_graph(), # 3-connected planar
               'truncated_tetrahedron': nx.truncated_tetrahedron_graph(), # 3-connected planar
               'tutte': nx.tutte_graph()}           # 3-connected planar
    for g_name, g in targets.items():
        tree_decomps = [maximum_cardinality_search(g), min_fill(g), min_degree(g)]
        draw(g, tree_decomps, h_names, g_name)
