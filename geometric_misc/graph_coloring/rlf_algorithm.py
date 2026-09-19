from heapq import heapify, heappop
import matplotlib.pyplot as plt
import networkx as nx


def rlf(_):
    """ Recursive largest first algorithm
            https://en.wikipedia.org/wiki/Recursive_largest_first_algorithm """
    g, S = _.copy(), []
    while g.order() != 0:
        s = {max((d, n) for n, d in g.degree)[1]}
        candidates = set(g) - s - set(_ for u in s for _ in g[u])
        while candidates:
            v = max((len(s & set(iter(g[c]))), c) for c in candidates)[1]
            s.add(v)
            candidates -= set(iter(g[v])) | set([v])
        g.remove_nodes_from(s)
        S.append(s)
    colors = {v: i for i, ic in enumerate(S) for v in ic}
    return [colors[v] for v in _]


def dsatur(g):
    """ DSatur: Graph coloring based on 'Degree of Saturation'
            https://en.wikipedia.org/wiki/DSatur """
    satur = {v: 0 for v in g}
    states = [(0, -d, v) for v, d in g.degree]
    tbl = {v: (s, d, v) for s, d, v in states}
    colors = {}
    while states:
        heapify(states)
        s, d, v = heappop(states)
        c = __get_color(satur[v])
        colors[v], b = c, 1 << c
        for u in g[v]:
            if u in colors:
                continue
            s, d, _ = tbl[u]
            satur[u] = satur[u] if (satur[u] >> c) & 1 else satur[u] + b 
            tbl[u] = (-satur[u].bit_count(), d+1, u)
        del tbl[v]
        states = list(tbl.values())
    return [colors[v] for v in g]


def __get_color(x):
    i = 0
    while x >> i:
        if (x >> i) & 1 == 0:
            return i
        i += 1
    return i


if __name__ == '__main__':
    g = nx.wheel_graph(9)
#    g = nx.frucht_graph()

    pos = nx.spring_layout(g)
    cmap = plt.get_cmap('tab10')
    colors = [[cmap(c+1) for c in rlf(g)], [cmap(c+1) for c in dsatur(g)]]
    _, axes = plt.subplots(1, 2, figsize=(10, 5))

    for ax, c in zip(axes, colors):
        nx.draw_networkx_nodes(g, pos, ax=ax, node_color=c).set_edgecolor('k')
        nx.draw_networkx_edges(g, pos, ax=ax)
        nx.draw_networkx_labels(g, pos, ax=ax)

        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    plt.show()
