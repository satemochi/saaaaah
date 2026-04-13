from collections import defaultdict, deque
from random import random, seed
from unittest import TestCase
from matplotlib import pyplot as plt
import networkx as nx


def bellman_ford(g, w, s):
    """ Bellman-Ford for the SSSP problem
        ref. networkx!
            `single_source_bellman_ford`, more preceisely,
            `_inner_bellman_ford` """
    dist, pred = defaultdict(lambda: float('inf')), {s: None}
    dist[s] = 0
    q, in_q, count = deque([s]), set([s]), defaultdict(lambda: 0)
    while q:
        in_q.remove((u := q.popleft()))
        if pred[u] not in in_q:
            dist_u = dist[u]
            for v in g[u]:
                if (dist_v := dist_u + w[u, v]) < dist[v]:
                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count[v] += 1
                        if count[v] == g.order():
                            raise Exception("Negative cost cycle detected.")
                    pred[v], dist[v] = u, dist_v
    return pred, dist


def bellman_ford2(g, w, s):
    dist, pred = defaultdict(lambda: float('inf')), {s: None}
    q, in_q = deque([s]), defaultdict(lambda: False)
    count, n = defaultdict(lambda: 0), g.order()
    dist[s], in_q[s] = 0, True
    while q:
        in_q[(u := q.popleft())] = False
        dist_u = dist[u]
        for v in g[u]:
            if (dist_v := dist_u + w[u, v]) < dist[v]:
                pred[v], dist[v] = u, dist_v
                if not in_q[v]:
                    q.append(v)
                    in_q[v] = True
                    count[v] += 1
                    if count[v] == n:
                        raise Exception("[negative cycle]")
    return pred, dist


class TestBellmanFord(TestCase):
    def test_trivial(self):
        g = nx.Graph()
        g.add_node(0)
        weight = {}
        pred, dist = bellman_ford(g, weight, 0)
        self.assertEqual(pred[0], None)
        self.assertTrue(dist[0] == 0)

    def test_frucht_non_negative_weight(self):
        seed(0)
        g = nx.frucht_graph()
        weight = {}
        for u, v in g.edges:
            weight[u, v] = random()
            weight[v, u] = weight[u, v]
        pred, dist = bellman_ford(g, weight, 0)
        self.assertEqual(pred[0], None)
        self.assertTrue(pred[1] == 0)

    def test_frucht_has_negative_weight(self):
        seed(0)
        g = nx.frucht_graph()
        weight = {}
        for u, v in g.edges:
            weight[u, v] = random()
            weight[v, u] = weight[u, v]
        weight[6, 10] = -weight[6, 10]
        weight[10, 6] = weight[6, 10]
        with self.assertRaises(Exception):
            pred, dist = bellman_ford(g, weight, 0, heuristic=True)
#            pred, dist = bellman_ford(g, weight, 0)

    def test_small_negative_weight(self):
        g = nx.Graph([(0, 1), (1, 2), (2, 3), (3, 1)])
        weight = {(0, 1): 4, (1, 0): 4, (1, 2): -6, (2, 1): -6,
                  (2, 3): 5, (3, 2): 5, (1, 3): -2, (3, 1): -2}
        with self.assertRaises(Exception):
            pred, dist = bellman_ford(g, weight, 0, heuristic=True)


def gen(_seed=0):
    seed(_seed)
    g = nx.frucht_graph()
    weight = {}
    for u, v in g.edges:
        weight[u, v] = random()
        weight[v, u] = weight[u, v]
    return g, weight, 0


if __name__ == '__main__':
    g, w, s = gen()
    pred, dist = bellman_ford(g, w, s)
#    from pprint import pprint
#    pprint(w)
#    pprint(pred)
#    pprint(dist)
    st = nx.Graph([(u, v) for u, v in pred.items() if u != s])

    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_nodes(g, pos, nodelist=[s],
                           node_color='#ccccff').set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_edges(st, pos, edge_color='r', width=3)
    nx.draw_networkx_labels(g, pos)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
