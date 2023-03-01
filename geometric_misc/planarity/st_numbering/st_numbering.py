from functools import reduce
import networkx as nx


def st_numbering(g, s, t):
    (low, parent, preorder), sign = __dfs(g, s, t), {s: False}
    pred, succ = {s: -float('inf'), t: s}, {s: t, t: float('inf')}   # as list
    for v in preorder:
        if sign[low[v]] is False:
            __insert(v, pred[parent[v]], pred, succ)
            sign[parent[v]] = True
        else:
            __insert(v, parent[v], pred, succ)
            sign[parent[v]] = False
    return __numbering(succ, s)


def __dfs(g, s, t):
    po, low, parent, stack = __init(g, s, t)
    while stack:
        x, children = stack[-1]
        try:
            y = next(children)
            if po[y] < 0:   # (x, y) is tree edge
                low[y], po[y], parent[y] = y, po[x] + 1, x
                stack.append((y, iter([v for v in g[y] if v != x])))
            elif po[y] < po[low[x]]:   # back edge
                low[x] = y
        except StopIteration:
            if po[low[x]] < po[low[parent[x]]]:
                low[parent[x]] = low[x]
            stack.pop()
    preorder = iter(low)
    next(preorder), next(preorder)  # ommitting s and t from pre-order
    return low, parent, preorder


def __init(g, s, t):
    po, low, parent = {v: -1 for v in g}, {}, {}
    (po[s], po[t]), (low[s], low[t]), parent[t] = (0, 1), (s, s), s
    return po, low, parent, [(t, iter([v for v in g[t] if v != s]))]


def __insert(v, u, pred, succ):
    pred[v], succ[v] = u, succ[u]
    pred[succ[u]], succ[u] = v, v


def __numbering(succ, v):
    n = {}
    for i in range(len(succ)):
        n[v], v = i, succ[v]
    return n


def __orient(g, n):
    return reduce(lambda x, v: x+[(v, w) for w in g[v] if n[v] < n[w]], g, [])


if __name__ == '__main__':
    g = nx.frucht_graph()
    print(numbering := st_numbering(g, s := 0, t := 9))

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g)
    n = nx.draw_networkx_nodes(g, pos, node_color="#ffcccc")
    n.set_edgecolor('k')

    n = nx.draw_networkx_nodes(g, pos, nodelist=[s, t], node_color="#ccffcc")
    n.set_edgecolor('k')
    edges = __orient(g, numbering)
    nx.draw_networkx_edges(g, pos, edgelist=edges, edge_color='r', arrows=True)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
#    plt.savefig('st_numbering_bipolar_orientation.png', bbox_inches='tight')
    plt.show()
