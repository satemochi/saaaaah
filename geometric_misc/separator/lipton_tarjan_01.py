from itertools import combinations
from random import random, sample, seed
from matplotlib import pyplot as plt
import networkx as nx
import triangle


class dt:
    def __init__(self, pts):
        self._t = triangle.triangulate(pts)
        self._g = self._get_nx_graph()
        self._d, self._bi = self._get_dual()    # dual graph/ bijectional map
        self._r, self._bfs, self._dt = self.__tree()
        self._cs = self.__separator()

    def _get_nx_graph(self):
        g = nx.Graph()
        for p, q, r in self.triangles:
            g.add_edges_from(((p, q), (q, r), (r, p)))
        return g

    def _get_dual(self):
        dual = nx.Graph()
        biject = {}
        for f, g in combinations(self.triangles, 2):
            if len(i := (set(f) & set(g))) > 1:
                biject[self.__reg(i)] = (tuple(f), tuple(g))
                biject[(tuple(f), tuple(g))] = self.__reg(i)
                dual.add_edge(tuple(f), tuple(g))
        dummy = (float('inf'), float('inf'), float('inf'))
        dual.add_edges_from([(v, dummy) for v in dual if len(dual[v]) <= 2])
        for a, b, c in dual:
            for e in ((a, b), (b, c), (c, a)):
                if self.__reg(e) not in biject:
                    biject[self.__reg(e)] = ((a, b, c), dummy)
                    biject[((a, b, c), dummy)] = self.__reg(e)
        return dual, biject

    @staticmethod
    def __reg(e):   # regulating for the edge-ordering
        return tuple(sorted(e))

    def __tree(self):
        r = self.__random_root(self._g)
        bfs = nx.bfs_tree(self._g, r).to_undirected()
        de = [self._bi[self.__reg(e)] for e in self._g.edges
              if e not in bfs.edges]
        return r, bfs, self._d.edge_subgraph(de)

    @staticmethod
    def __random_root(g):
        return sample(g.nodes, 1)[0]

    def __separator(self):
        x, y = self.__balanced_bridge()
        e = self._bi[(x, y)] if (x, y) in self._bi else self._bi[(y, x)]
        return self.__disjoint_cycle(*e)

    def __balanced_bridge(self):
        r, n = self.__subtree_count()
        threshold = (2 * self._dt.order() + 1) // 3
        checked = [r]
        vi = max((n[v], v) for v in self._dt[r])[1]
        e = (r, vi)
        while n[vi] > threshold:
            checked.append(vi)
            vi = max((n[v], v) for v in self._dt[vi] if v not in checked)[1]
            e = (e[1], vi)
        return e

    def __subtree_count(self):
        r = self.__random_root(self._dt)
        n, checked = {v: 1 for v in self._dt}, [r]
        stack = [(r, iter(self._dt[r]))]
        while stack:
            x, children = stack[-1]
            try:
                y = next(children)
                if y not in checked:
                    stack.append((y, iter(self._dt[y])))
                    checked.append(y)
            except(StopIteration):
                stack.pop()
                if stack:
                    n[stack[-1][0]] += n[x]
        return r, n

    def __disjoint_cycle(self, x, y):
        xp = nx.shortest_path(self._bfs, source=self._r, target=x)
        yp = nx.shortest_path(self._bfs, source=self._r, target=y)
        lowest_common = self._r
        for i, (xi, yi) in enumerate(zip(xp[1:], yp[1:]), start=1):
            if xi == yi:
                lowest_common = xi
            else:
                break
        return [lowest_common] + xp[i:] + list(reversed(yp[i:]))

    def draw_planar_graph(self):
        nx.draw(self.planar_graph, self.vertices, node_size=20, alpha=0.25)
        # nx.draw_networkx_labels(self._bfs, self.vertices)

    def draw_dual(self):
        pos = {f: self.__c(f) for f in self._d}
        dummy = (float('inf'), float('inf'), float('inf'))
        el = [e for e in self._d.edges if dummy not in e]
        nx.draw(self._d, pos, node_size=8, #edgelist=el,
                node_color='orange', edge_color='pink')

    def __c(self, f):   # return geometric center for a bounded face
        if float('inf') in f:
            return (2, 2)
        return (sum(self.vertices[i][0] for i in f) / 3,
                sum(self.vertices[i][1] for i in f) / 3)

    def draw_minimum_spanning_tree(self):
        nx.draw(self._bfs, self.vertices, node_size=20, edge_color='#8888ff')
        # pos = {f: self.__c(f) for f in self._d}
        # nx.draw(self._dt, pos, node_size=20, edge_color='#8888ff')

    def __dist(self, u, v):
        p, q = self.vertices[u], self.vertices[v]
#        return sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)
        return ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5

    def draw_cycle_separator(self):
        n = len(self._cs)
        ce = [(self._cs[i], self._cs[(i+1) % n]) for i in range(n)]
        nx.draw(self._g, self.vertices, nodelist=self._cs, edgelist=ce,
                node_size=20, node_color='r', edge_color='r')
        sg = self._g.subgraph([v for v in self._g if v not in self._cs])
        print(f'separator size: {len(self._cs)}')
        for c, col in zip(nx.connected_components(sg), ['#ffcccc', '#ccccff']):
            nodes = nx.draw_networkx_nodes(self._g, self.vertices, nodelist=c,
                                           node_size=20, node_color=col)
            nodes.set_edgecolor('black')
            print(len(c))

    @property
    def vertices(self):
        return self._t['vertices']

    @property
    def triangles(self):
        return self._t['triangles']

    @property
    def planar_graph(self):
        return self._g

    @property
    def dual_graph(self):
        return self._d

    @property
    def edge_map(self):
        return self._bi

    @property
    def minimum_spanning_tree(self):
        return self._bfs

    @property
    def dual_minimum_spanning_tree(self):
        return self._dt

    @property
    def separator(self):
        return self._cs


#def gen(n=300, s=6):
def gen(n=300, s=None):
    seed(s)
    return {'vertices': [(random(), random()) for i in range(n)]}


if __name__ == '__main__':
    pts = gen()
    t = dt(pts)

    t.draw_planar_graph()
#    t.draw_dual()
#    t.draw_minimum_spanning_tree()
    t.draw_cycle_separator()

    plt.gca().set_aspect('equal')
#    plt.savefig('cycle_separator_01.png', bbox_inches='tight')
    plt.show()
