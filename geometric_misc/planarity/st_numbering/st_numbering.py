import networkx as nx


def st_numbering(g, s, t):
    low, parent, preorder = __dfs(g, s, t)
    sign = {s: False}
    pre, post = {s: -1, t: s, float('inf'): t}, {-1: s, s: t, t: float('inf')}
    for v in preorder:
        if sign[low[v]] is False:
            __insert(v, pre[parent[v]], pre, post)
            sign[parent[v]] = True
        else:
            __insert(v, parent[v], pre, post)
            sign[parent[v]] = False
    return __numbering(post, s)


def __dfs(g, s, t):
    po, low, parent, stack = __init(g, s, t)
    while stack:
        x, children = stack[-1]
        try:
            y = next(children)
            if po[y] < 0:   # (x, y) is tree edge
                low[y] = y
                po[y] = po[x] + 1
                parent[y] = x
                stack.append((y, iter([v for v in g[y] if v != x])))
            elif po[y] < po[low[x]]:   # back edge
                low[x] = y
        except StopIteration:
            if po[low[x]] < po[low[parent[x]]]:
                low[parent[x]] = low[x]
            stack.pop()
    preorder = iter(low)
    next(preorder), next(preorder)
    return low, parent, preorder


def __init(g, s, t):
    po, low, parent = {v: -1 for v in g}, {}, {}
    po[s], po[t] = 0, 1
    low[s], low[t] = s, s
    parent[t] = s
    return po, low, parent, [(t, iter([v for v in g[t] if v != s]))]


def __insert(v, pos, pre, post):
    # assert(pos in pre and pos in post)
    pre[v], post[v] = pos, post[pos]
    pre[post[pos]], post[pos] = v, v


def __numbering(post, v):
    n = {}
    for i in range(len(post)-1):
        n[v], v = i, post[v]
    return n


def __orient(g, n):
    edges = []
    for v in g:
        edges += [(v, w) for w in g[v] if n[v] < n[w]]
    return edges


if __name__ == '__main__':
    g = nx.frucht_graph()
    print(numbering := st_numbering(g, s := 0, t := 9))

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g)
    n = nx.draw_networkx_nodes(g, pos, node_color="#ffcccc")
    n.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)

    n = nx.draw_networkx_nodes(g, pos, nodelist=[s, t], node_color="#ccffcc")
    n.set_edgecolor('k')
    edges = __orient(g, numbering)
    nx.draw_networkx_edges(g, pos, edgelist=edges, edge_color='r', arrows=True)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig('st_numbering_bipolar_orientation.png', bbox_inches='tight')
    plt.show()
