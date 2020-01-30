from abc import ABCMeta, abstractmethod
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from pulp import LpVariable, LpProblem, lpSum, lpDot


__all__ = ['ordinary_mtz', 'enhanced_mtz',
           'lazy_generation', 'lazy_generation2']


class _tsp(metaclass=ABCMeta):
    """ TSP interface (one shot) """
    def __init__(self, P):
        g = self._associated_graph(P)
        # print(type(self).__name__)
        self.__tour = self._get_tour(g)
        # g.clear()

    @staticmethod
    def _associated_graph(P):
        g = nx.complete_graph(len(P), create_using=nx.DiGraph)
        for u, v in g.edges:
            g[u][v]['v'] = LpVariable('x%d,%d' % (u, v), cat='Binary')
            g[u][v]['w'] = np.linalg.norm(P[u] - P[v])
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
        for v in g:
            lp += lpSum(g[v][w]['v'] for w in g.successors(v)) == 1
            lp += lpSum(g[u][v]['v'] for u in g.predecessors(v)) == 1
        for u, v in g.edges:    # this is for Dantzig-Fulkerson-Johnson.
            if u < v:
                lp += g[u][v]['v'] + g[v][u]['v'] <= 1
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
        for u in g:
            if u != 0:
                g.nodes[u]['v'] = LpVariable('u%d' % (u), 1, len(P)-1)
        return g

    def _get_tour(self, g):
        self._mtz_formulation(g).solve()
        tour = [0] * g.order()
        for v in range(1, g.order()):
            tour[int(g.nodes[v]['v'].varValue)] = v
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
        See following web-slide (p. 33) due to M. Kubo.

            https://www.slideshare.net/MikioKubo/gurobi-python
    """
    def _mtz_formulation(self, g):
        n, lp = g.order(), self._init_formulation(g)
        lp += g.nodes[0]['v'] == 0
        for i, j in g.edges:
            if 0 not in (i, j):
                lp += (g.nodes[i]['v'] - g.nodes[j]['v'] + (n-1)*g[i][j]['v']
                       + (n-3)*g[j][i]['v'] <= n-2)
        for i in g:
            if i == 0:
                continue
            lp += 2 - g[0][i]['v'] + (n-3)*g[i][0]['v'] <= g.nodes[i]['v']
            lp += g.nodes[i]['v'] <= n-2 + g[i][0]['v'] - (n-3)*g[0][i]['v']
        return lp


class lazy_generation(_tsp):
    """ A subtour elimination by using lazy constraint generation: cf.

        https://cnc-selfbuild.blogspot.com/2019/06/tsp-lp-lazy-subtour-elimination.html
    """
    def _get_tour(self, g):
        lp, subtours = self._init_formulation(g), []
        while len(subtours) != 1:
            self._build_and_scrap(g, lp, subtours)
            subtours = self.__get_subtours(g)
        return subtours.pop()

    def _build_and_scrap(self, g, lp, subtours=None):
        if subtours is not None:
            for s in subtours:
                if len(s) > g.order() / 2:
                    continue
                self._bridging(g, lp, s)
        lp.solve()

    @staticmethod
    def _bridging(g, lp, s):
        lp += lpSum(g[u][v]['v'] for u in s for v in g.predecessors(u)
                    if v not in s) >= 1

    @staticmethod
    def __get_subtours(g):
        subtours, visited, succ = [], {v: False for v in g}, g.successors
        for v in g:
            if visited[v]:
                continue
            tour = []
            while v not in tour:
                tour.append(v)
                visited[v] = True
                v = next(w for w in succ(v) if g[v][w]['v'].varValue > 0)
            subtours.append(tour)
        return subtours


class lazy_generation2(lazy_generation):
    """ A subtour elimination by using lazy constraint generation: cf.

        P. Ulrich, S. Rostislav: (2017)
            "Generating subtour elimination constraints for the TSP from
             pure integer solutions"
        Central European journal of operations research, 25(1), pp. 231--260.
    """
    def _build_and_scrap(self, g, lp, subtours=None):
        if subtours is not None:
            for s in subtours:
                if len(s) < (2*g.order() + 1) / 2:
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
        t = s[1:] + [s[0]]
        lp += lpSum(g[u][v]['v'] for u, v in zip(s, t)) <= len(s) - 1
        lp += lpSum(g[v][u]['v'] for u, v in zip(s, t)) <= len(s) - 1


def draw(P, tours):
    _, axs = plt.subplots(1, len(tours), figsize=(12, 4))
    n, styles = len(P), ('go-', 'bo-', 'ro-', 'gx-', 'bx-', 'rx-')
    for t, ax, style in zip(tours, axs, styles):
        for i in range(n):
            ax.plot(P[[t[i], t[(i+1) % n]], 0],
                    P[[t[i], t[(i+1) % n]], 1], style)
        ax.set_aspect('equal')
        ax.axis('off')
    plt.tight_layout()


def gen(n=10, seed=None):
    np.random.seed(seed)
    return np.random.random((n, 2))


def length(P, tour):
    n = len(P)
    return sum(np.linalg.norm(P[tour[i]] - P[tour[(i+1) % n]])
               for i in range(n))


if __name__ == '__main__':
    P = gen(15)
    m, l1, l2 = enhanced_mtz(P), lazy_generation(P), lazy_generation2(P)
#    m, l1, l2 = ordinary_mtz(P), lazy_generation(P), lazy_generation2(P)
    draw(P, [m.tour, l1.tour, l2.tour])
    print(length(P, m.tour), length(P, l1.tour), length(P, l2.tour))
    plt.show()
