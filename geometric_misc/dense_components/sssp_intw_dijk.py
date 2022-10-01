from collections import defaultdict
import networkx as nx
from pprint import pprint


def a(g, s, t, w, lmax):
    # assert(g.has_node(s) and g.has_node(t) and s != t)
    unmarked, current_dist, wave_front, dmin, prev = __init(g, s, w, lmax)
    while 1:
        unmarked[(u := wave_front[dmin].pop())] = False
        for v in (_ for _ in g[u] if unmarked[_]):
            duv = current_dist[u] + w[u, v]
            if duv < dmin:
                dmin = duv
            if duv < current_dist[v]:
                wave_front[current_dist[v]].remove(v)
            if current_dist[v] < 0 or duv < current_dist[v]:
                current_dist[v], prev[v] = duv, u
                wave_front[current_dist[v]].add(v)
        if not wave_front[dmin]:
            try:
                dmin = next(i for i in range(dmin+1, dmin+lmax)
                            if wave_front[i])
            except StopIteration:
                break
    return current_dist


def __init(g, s, w, lmax):
    unmarked, current_dist = defaultdict(lambda: True), {v: -1 for v in g}
    unmarked[s], current_dist[s] = False, 0
    dmin, prev, wave_front = lmax, {}, defaultdict(set)
    for v in g[s]:
        current_dist[v], prev[v] = w[s, v], s
        if current_dist[v] < dmin:
            dmin = current_dist[v]
        wave_front[current_dist[v]].add(v)
    return unmarked, current_dist, wave_front, dmin, prev


def gen(mi=1, ma=20):
    g = nx.frucht_graph()
    from random import randint, seed
    seed(0)
    w = {e: randint(1, ma) for e in g.edges}
    nx.set_edge_attributes(g, w, 'weight')
    for u, v in g.edges:
        w[v, u] = w[u, v]
    return g, w


if __name__ == '__main__':
    g, w = gen()
    pprint(w)
    print(a(g, 0, 9, w, 10))

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc')
    nodes.set_edgecolor('k')

    s, t = 0, 9
    nx.draw_networkx_nodes(g, pos, nodelist=[s, t], node_color=['g', 'r'])
    sp = nx.shortest_path(g, 0, 9, weight='weight')
    nx.draw_networkx_edges(g, pos, edge_color='r',
                           edgelist=[(p, q) for p, q in zip(sp, sp[1:])])

    edges = nx.draw_networkx_edges(g, pos, alpha=0.3)
    edges.set_zorder(-10)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edge_labels(g, pos, nx.get_edge_attributes(g, 'weight'))

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('sssp_intw_dijk.png', bbox_inches='tight', transparent=True)
    plt.show()
