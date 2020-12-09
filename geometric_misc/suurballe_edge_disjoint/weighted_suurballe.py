from random import seed
from matplotlib import pyplot as plt
import networkx as nx

def suurballe(g, s=0, t=1):
    h = g.to_directed()
    lengths, paths = nx.single_source_dijkstra(h, s)
    for u, v in h.edges:
        g[u][v]['weight'] += lengths[u] - lengths[v]
    p1 = [e for e in zip(paths[t], paths[t][1:])]
    h.remove_edges_from(p1)
    p = nx.dijkstra_path(h, s, t)
    return _trim_duplicates(p1, [e for e in zip(p, p[1:])])


def _trim_duplicates(p1, p2):
    g = nx.DiGraph(p1 + p2)
    for u, v in p1:
        if g.has_edge(v, u):
            g.remove_edges_from([(u, v), (v, u)])
    q = nx.dijkstra_path(g, p1[0][0], p1[-1][-1])
    q1 = [e for e in zip(q, q[1:])]
    g.remove_edges_from(q1)
    q2 = nx.dijkstra_path(g, p1[0][0], p1[-1][-1])
    return q1, [e for e in zip(q2, q2[1:])]


def __weight_assign(g):
    for x, y in g.edges:
        p, q = g.nodes[x]['pos'], g.nodes[y]['pos']
        g[x][y]['weight'] = ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5


def __draw_shortest_path(g, s, t):
    p = nx.dijkstra_path(g, s, t)
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw_networkx_edges(g, pos, edgelist=[e for e in zip(p, p[1:])],
                           edge_color='r', width=1.75, alpha=.75)


if __name__ == '__main__':
    seed(0)
    g = nx.random_geometric_graph(70, 0.2)

    __weight_assign(g)

    pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos, node_color='#ffcccc', alpha=0.35)
    nx.draw_networkx_labels(g, pos)

#    __draw_shortest_path(g, 17, 47)
#    h = g.to_directed()
#    from pprint import pprint
#    pprint(nx.get_edge_attributes(h, 'weight'))

    p1, p2 = suurballe(g, s=48, t=20)
    print(p1)
    print(p2)

    nx.draw_networkx_edges(g, pos, edgelist=p1, edge_color='r', width=1.5)
    nx.draw_networkx_edges(g, pos, edgelist=p2, edge_color='b', width=1.5)

    plt.gca().set_aspect('equal')
    plt.savefig('weighted_suurballe_01.png', bbox_inches='tight')
    plt.show()
