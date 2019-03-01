import networkx as nx
from constraint_list import constraint_list


def is_planar(g):
    if g.size() < 9 or g.order() < 5:
        return True
    if g.size() > 3 * g.order() - 6:
        return False
    for v in g.nodes():
        if 'visited' not in g.node[v]:
            g.node[v]['visited'] = True
            if not lr_algorithm(g, v):
                return False
    return True


def lr_algorithm(g, root):
    conflict_pairs = [[]]
    tree_edges = []
    dfsnum = [1] * g.order()
    dfs_stack = [(root, iter(g[root]))]
    while dfs_stack:
        v, children = dfs_stack[-1]
        try:
            w = next(children)
            if 'visited' in g[v][w]:
                continue
            g[v][w]['visited'] = True
            if 'visited' in g.node[w]:
                if dfsnum[v] > dfsnum[w]:   # back edge
                    conflict_pairs[-1].append(constraint_list(dfsnum[w]))
            else:                           # tree edge
                dfsnum[w] = dfsnum[v] + 1
                g.node[w]['visited'] = True
                tree_edges.append((v, w))
                conflict_pairs.append([])
                dfs_stack.append((w, iter(g[w])))
        except StopIteration:
            dfs_stack.pop()
            if len(conflict_pairs) > 1:
                _, w = tree_edges.pop()
                print '======backtracking=====', (_, w)
                print conflict_pairs
                print tree_edges

                mcl = merge_constraint_lists(conflict_pairs[-1], dfsnum[w])
                if mcl is None:
                    return False
                conflict_pairs.pop()
                if len(mcl) > 0:
                    conflict_pairs[-1].append(mcl)
    return True


def merge_constraint_lists(vcl, dfs_height):
    mcl = []
    if len(vcl) > 0:
        print '-- merge_cl:', vcl
        vcl.sort()
        print '-- merge_cl: sorted', vcl
        vcl[0], mcl = mcl, vcl[0]
        for i in xrange(1, len(vcl)):
            if not mcl.merge(vcl[i]):
                return None
        mcl.prune(dfs_height)
    return mcl


def clean_attributes(g):
    for v in g.nodes():
        if 'visited' in g.node[v]:
            del g.node[v]['visited']
    for u, v in g.edges():
        if 'visited' in g[u][v]:
            del g[u][v]['visited']


if __name__ == '__main__':
#    g = nx.petersen_graph()
    g = nx.frucht_graph()
#    g = nx.krackhardt_kite_graph()
#    g = nx.icosahedral_graph()
#    g = nx.tutte_graph()
#    g = nx.chvatal_graph()
#    g = nx.desargues_graph()

    print is_planar(g)
#    from matplotlib import pyplot as plt
#    nx.draw_networkx(g)
#    plt.show()
