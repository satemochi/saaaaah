from itertools import permutations
import subprocess
from matplotlib import pyplot as plt
import networkx as nx


def draw_all_dfs_ordering(g, pos=None):
    if pos is None:
        pos = nx.spring_layout(g)
    counter = 0
    for o in permutations(g.nodes(), g.order()):
        if is_dfs_ordering(g, o):
            counter += 1
            print counter, o
            plt.cla()
            nx.draw_networkx_edges(g, pos, alpha=0.2)
            nx.draw_networkx_nodes(g, pos)
            nx.draw_networkx_labels(g, pos)
            draw_tree_edges(g, pos, o)
            plt.gca().set_title(str(o))
            plt.gca().set_aspect('equal')
            plt.gca().axis('off')
            plt.savefig('dfs_ordering_' + str(counter).zfill(4) + '.png',
                        bbox_inces='tight')


def is_dfs_ordering(graph, ordering):
    n = len(ordering)
    for i in xrange(1, n-1):
        sub_ordering = ordering[:i]
        x = greatest_incident_index(g, sub_ordering, ordering[i])
        y = max(greatest_incident_index(g, sub_ordering, ordering[j])
                for j in xrange(i+1, n))
        if x < y:
            return False
    return is_last_edge_in_graph(g, ordering)


def greatest_incident_index(g, sub_ordering, v):
    return max(i if u in g[v] else -1 for i, u in enumerate(sub_ordering))


def is_last_edge_in_graph(g, ordering):
    v = ordering[-1]
    u = ordering[greatest_incident_index(g, ordering, v)]
    return g.has_edge(u, v)


def draw_tree_edges(g, pos, ordering):
    t = nx.DiGraph()
    for i in reversed(xrange(1, len(ordering))):
        v = ordering[i]
        u = ordering[greatest_incident_index(g, ordering[:i], v)]
        t.add_edge(u, v)
    nx.draw_networkx_edges(t, pos, arrowstyle='->', arrowsize=10)


if __name__ == '__main__':
    g = nx.bull_graph()
#    g = nx.frucht_graph()
#    g = nx.petersen_graph()
#    g = nx.house_graph()
    draw_all_dfs_ordering(g)
    cmd = 'convert -delay 120 -layers Optimize dfs_o*.png dfs_ordering.gif'
    subprocess.call(cmd, shell=True)
    subprocess.call('rm dfs_o*.png', shell=True)
