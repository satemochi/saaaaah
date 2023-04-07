from matplotlib import pyplot as plt
import networkx as nx


def et(g):
    assert(is_eulerian(g))
    g, s = g.copy(), next(iter(g))
    _stack, last_vertex = [s], None
    while _stack:
        current_vertex = _stack[-1]
        if g.degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex)
            last_vertex = current_vertex
            _stack.pop()
        else:
            next_vertex = next(iter(g[current_vertex]))
            g.remove_edge(current_vertex, next_vertex)
            _stack.append(next_vertex)

            # e = (current_vertex, next_vertex)
            # nx.draw_networkx_edges(g, pos, edgelist=[e],
            #                        edge_color='#55ff55')
            # plt.draw()
            # plt.pause(0.9)


def is_eulerian(g):
    return all(d & 1 == 0 for _, d in g.degree()) and is_connected(g)


def is_connected(g):
    return sum(1 for v in _bfs(g, next(iter(g)))) == g.order()


def _bfs(g, s):
    seen, nextlevel = set(), {s}
    while nextlevel:
        thislevel, nextlevel = nextlevel, set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel |= set(g[v])


if __name__ == '__main__':
    g = nx.chvatal_graph()

    pos = nx.spring_layout(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, edge_color='#cccccc')
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.axis('off')
    plt.tight_layout()

    for e in et(g):
        nx.draw_networkx_edges(g, pos, edgelist=[e], arrows=True, edge_color='g')
        plt.draw()
        plt.pause(0.9)

    # plt.savefig('et_01.png', bbox_inches='tight')
    plt.show()
