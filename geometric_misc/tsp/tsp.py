from abc import ABCMeta, abstractmethod
import networkx as nx
import numpy as np
from pulp import LpVariable, LpProblem, lpSum, lpDot


__all__ = ['ordinary_mtz', 'enhanced_mtz',
           'lazy_generation', 'lazy_generation2']


class _tsp(metaclass=ABCMeta):
    """ TSP interface (one shot) """
    def __init__(self, P):
        g = self._associated_graph(P)
        print(type(self).__name__)
        self.__tour = self._get_tour(g)
        g.clear()

    @staticmethod
    def _associated_graph(P):
        g = nx.complete_graph(len(P), create_using=nx.DiGraph)
        for i, j in g.edges:
            g[i][j]['v'] = LpVariable('x%d,%d' % (i, j), cat='Binary')
            g[i][j]['w'] = np.linalg.norm(P[i] - P[j])
        return g

    @abstractmethod
    def _get_tour(self):
        raise NotImplementedError()

    @property
    def tour(self):
        return self.__tour

    @staticmethod
    def _init_formulation(g):
        lp = LpProblem()
        lp += lpSum(lpDot(nx.get_edge_attributes(g, 'v').values(),
                          nx.get_edge_attributes(g, 'w').values()))
        for i in g:
            lp += lpSum(g[i][j]['v'] for j in g.successors(i)) == 1
            lp += lpSum(g[j][i]['v'] for j in g.predecessors(i)) == 1
        for i, j in g.edges:    # this is for Dantzig-Fulkerson-Johnson.
            if i < j:
                lp += g[i][j]['v'] + g[j][i]['v'] <= 1
        return lp


class ordinary_mtz(_tsp):
    """ The Miller-Tucker-Zemlin formula due to

        C.E. Miller, A.W. Tucker, and R.A. Zemlin: (1960)
            "Integer programming formulation of traveling salesman problems"
        Journal of the ACM, 7(4), pp. 326--329.
    """
    def _associated_graph(self, P):
        g = super()._associated_graph(P)
        g.nodes[0]['v'] = LpVariable('u0')
        for i in range(1, len(P)):
            g.nodes[i]['v'] = LpVariable('u%d' % (i), 1, len(P)-1)
        return g

    def _get_tour(self, g):
        self._mtz_formulation(g).solve()
        tour = [0] * g.order()
        for i in range(1, g.order()):
            tour[int(g.nodes[i]['v'].varValue)] = i
        return tour

    def _mtz_formulation(self, g):
        lp, n = self._init_formulation(g), g.order()
        lp += g.nodes[0]['v'] == 0
        for i, j in g.edges:
            if 0 in (i, j):
                continue
            lp += g.nodes[i]['v'] - g.nodes[j]['v'] + (n-1)*g[i][j]['v'] <= n-2
        return lp


class enhanced_mtz(ordinary_mtz):
    """ The Desrochers-Laporte formula due to

        M. Desrochers, G. Laporte: (1991)
            "Improvements and extensions to the Miller-Tucker-Zemlin subtour
             elimination constraints"
        Operations Research Letters, 10(1), pp. 27--36.

        In addition, we would like to apply constraints around the oringin.
        See following web-slide (p. 33) written by M. Kubo.

            https://www.slideshare.net/MikioKubo/gurobi-python
    """
    def _mtz_formulation(self, g):
        lp, n = self._init_formulation(g), g.order()
        lp += g.nodes[0]['v'] == 0
        for i, j in g.edges:
            if 0 not in (i, j):
                lp += (g.nodes[i]['v'] - g.nodes[j]['v'] + (n-1)*g[i][j]['v']
                       + (n-3)*g[j][i]['v'] <= n-2)
        for i in range(1, g.order()):
            lp += 2 - g[0][i]['v'] + (n-3)*g[i][0]['v'] <= g.nodes[i]['v']
            lp += g.nodes[i]['v'] <= n-2 + g[i][0]['v'] - (n-3)*g[0][i]['v']
        return lp


class lazy_generation(_tsp):
    """ A subtour elimination by using lazy generation: cf.

        https://cnc-selfbuild.blogspot.com/2019/06/tsp-lp-lazy-subtour-elimination.html
    """
    def _get_tour(self, g):
        lp, subtours = self._init_formulation(g), []
        while len(subtours) != 1:
            self._build_and_scrap(g, lp, subtours)
            subtours = self.__get_subtours(g)
        return subtours.pop()

    def _build_and_scrap(self, g, lp, subtours):
        if subtours is not None:
            for s in subtours:
                if len(s) < g.order() / 2:
                    self._bridging(g, lp, s)
        lp.solve()

    @staticmethod
    def _bridging(g, lp, s):
        lp += lpSum(g[i][j]['v'] for i in s for j in g.successors(i)
                    if j not in s) >= 1

    @staticmethod
    def __get_subtours(g):
        subtours, visited, succ = [], {v: False for v in g}, g.successors
        for v in g:
            if visited[v]:
                continue
            tour = []
            while not visited[v]:
                tour.append(v)
                visited[v] = True
                v = next(w for w in succ(v) if g[v][w]['v'].varValue > 0)
            subtours.append(tour)
        return subtours


class lazy_generation2(lazy_generation):
    """ A subtour elimination by using lazy generation: cf.

        P. Ulrich, S. Rostislav: (2017)
            "Generating subtour elimination constraints for the TSP from
             pure integer solutions"
        Central European journal of operations research, 25(1), pp. 231--260.
    """
    def _build_and_scrap(self, g, lp, subtours=None):
        if subtours is not None:
            for s in subtours:
                if len(s) < (2*g.order() + 1) / 3:
                    self._disconnecting(g, lp, s)
                else:
                    self._bridging(g, lp, s)
        lp.solve()

    @staticmethod
    def _disconnecting(g, lp, s):
        """ Traditional subtour elimination constraints due to

            G. Dantzig, R. Fulkerson, S. Johnson: (1954)
                "Solution of a large-scale traveling-salesman problem"
            Journal of the Operations Research society of America, 2(4),
            pp. 393--410.
        """
        lp += lpSum(g[u][v]['v'] for u, v in g.subgraph(s).edges) <= len(s)-1


def draw(P, tours):
    from matplotlib import pyplot as plt
    assert(len(tours) <= 6)
    _, axs = plt.subplots(1, len(tours), figsize=(12, 4))
    n, styles = len(P), ('go-', 'bo-', 'ro-', 'gx-', 'bx-', 'rx-')
    for t, ax, style in zip(tours, axs, styles):
        for i in range(n):
            ax.plot(P[[t[i], t[(i+1) % n]], 0],
                    P[[t[i], t[(i+1) % n]], 1], style)
        ax.set_aspect('equal')
        ax.axis('off')
    plt.tight_layout()
    # plt.savefig('tsp_lazy_generation_%d.png' % len(P), bbox_inches='tight')
    plt.show()


def gen(n=10, seed=None):
    np.random.seed(seed)
    return np.random.random((n, 2))


def length(P, tour):
    n = len(P)
    return sum(np.linalg.norm(P[tour[i]] - P[tour[(i+1) % n]])
               for i in range(n))


def eval(algo, pts):
    from time import time
    start = time()
    a = algo(pts)
    return a.tour, time() - start


if __name__ == '__main__':
    P = gen(15)
    m1, m2, lz = ordinary_mtz(P), enhanced_mtz(P), lazy_generation(P)
    print(length(P, m1.tour), length(P, m2.tour), length(P, lz.tour))
    draw(P, [m1.tour, m2.tour, lz.tour])

#    P = gen(100)
#    l1, t1 = eval(lazy_generation, P)
#    l2, t2 = eval(lazy_generation2, P)
#    print(t1, t2)
#    print(length(P, l1), length(P, l2))
#    draw(P, [l1, l2])
