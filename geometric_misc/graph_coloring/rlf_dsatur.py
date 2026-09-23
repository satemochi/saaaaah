from heapq import heapify, heappop, heappush
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
    sat, col = {v: 0 for v in g}, {}
    q, deg = [(0, -d, v) for v, d in g.degree], {v: -d for v, d in g.degree}
    heapify(q)
    while len(col) < g.order():
        s, d, v = heappop(q)
        if v in col or deg[v] > d:
            continue
        col[v] = __get_color(sat[v])
        b = 1 << col[v]
        for u in g[v]:
            deg[u] += 1
            if u not in col:
                if sat[u] & b:
                    heappush(q, (s, d+1, u))
                else:
                    sat[u] |= b
                    heappush(q, (s-1, d+1, u))
    return [col[v] for v in g]


def __get_color(x):     # should be binary search?
    i = 0
    while x >> i:
        if (x >> i) & 1 == 0:
            break
        i += 1
    return i


if __name__ == '__main__':
    # g = nx.wheel_graph(9)
    # g = nx.frucht_graph()
    g = nx.tutte_graph()

    pos = nx.spring_layout(g)
    cmap = plt.get_cmap('tab10')
    colors = [[cmap(c+1) for c in rlf(g)], [cmap(c+1) for c in dsatur(g)]]
    _, axes = plt.subplots(1, 2, figsize=(10, 5))

    for ax, c in zip(axes, colors):
        nx.draw_networkx_nodes(g, pos, ax=ax, node_size=45,
                               node_color=c).set_edgecolor('k')
        nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.5)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    # plt.savefig('rlf_dsatur.png', bbox_inches='tight')
    plt.show()
