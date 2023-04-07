from subprocess import call
from matplotlib import pyplot as plt
import networkx as nx


def et(g):
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

    for i, e in enumerate(et(g)):
        nx.draw_networkx_edges(g, pos, edgelist=[e], arrows=True, edge_color='g')
        plt.savefig('_'+str(i).zfill(2)+'.png', bbox_inches='tight')

    cmd = 'convert -delay 100 -layers Optimize _*.png euler_tour_anim.gif'
    call(cmd, shell=True)
    call('rm _*.png', shell=True)
