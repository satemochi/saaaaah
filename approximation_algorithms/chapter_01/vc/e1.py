import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
from networkx.algorithms.approximation import min_maximal_matching
from matplotlib import pyplot as plt
from itertools import izip
import math
import random
import numpy as np


def gen():
# predefined graphs in networkx
#    return nx.bull_graph()              # 1-connected planar
#    return nx.chvatal_graph()           # 4-connected non-planar
#    return nx.cubical_graph()           # 3-connected planar
#    return nx.desargues_graph()         # 3-connected non-planar
#    return nx.diamond_graph()           # 2-connected planar
#    return nx.dodecahedral_graph()      # 3-connected planar
#    return nx.frucht_graph()            # 3-connected planar
#    return nx.heawood_graph()           # 3-connected planar
#    return nx.house_graph()             # 2-connected planar
#    return nx.house_x_graph()           # 2-connected planar
#    return nx.icosahedral_graph()       # 5-connected planar
#    return nx.krackhardt_kite_graph()   # 1-connected planar
#    return nx.moebius_kantor_graph()    # non-planar
#    return nx.octahedral_graph()        # 4-connected planar
#    return nx.pappus_graph()            # 3-connected non-planar
    return nx.petersen_graph()          # 3-connected non-planar
#    return nx.sedgewick_maze_graph()    # 1-connected planar
#    return nx.tetrahedral_graph()       # 3-connected planar
#    return nx.truncated_cube_graph()    # 3-connected planar
#    return nx.truncated_tetrahedron_graph() # 3-connected planar
#    return nx.tutte_graph()             # 3-connected planar



def get_cycle(g, mi=None):
    cb = nx.cycle_basis(g)
    if not mi or mi >= len(cb):
        argmax = lambda array: max(izip(array, xrange(len(array))))[1]
        mi = argmax([len(c) for c in cb])
    return cb[mi]


def fix_outer_cycle_pos(g, cycle_vertices):
    rad = 2 * math.pi / len(cycle_vertices)
    for i, v in enumerate(cycle_vertices):
        g.node[v]['coord'] = (math.cos(rad * i), math.sin(rad * i))


def fix_all_pos(g):
    # building coefficient-matrices for xy-coordinates of the unfixed vertices
    A, Bx, By = [], [], []
    for v in g.nodes_iter():
        a = [0] * nx.number_of_nodes(g)
        bx, by = 0, 0
        if 'coord' in g.node[v]:    # a fixed vertex which is constant
            a[v] = 1
            bx = g.node[v]['coord'][0]
            by = g.node[v]['coord'][1]
        else:
            a[v] = len(g[v])
            for n in g[v]:      # for neighbors
                a[n] = -1       # to be the barycenter constraint
        A.append(a)
        Bx.append(bx)
        By.append(by)
    # solving systems of linear equations
    xcoords = np.linalg.solve(A, Bx)
    ycoords = np.linalg.solve(A, By)
    # asigning coordinates
    for v, coord in enumerate(zip(xcoords, ycoords)):
        g.node[v]['coord'] = coord


def draw(g, ax=None, title=None, vl=None, el=None):
    if not ax:
        ax = plt.gca()
    pos = nx.get_node_attributes(g, 'coord')
    nx.draw_networkx(g, pos=pos, ax=ax, node_color='g', with_labels=False,
                     node_size=20)
    if vl:
        nx.draw_networkx_nodes(g, pos=pos, ax=ax, node_color='r',
                               with_labels=False, node_size=50, nodelist=vl)
    if el:
        nx.draw_networkx_edges(g, pos=pos, ax=ax, edge_color='r', width=3,
                               edgelist=el)
    ax.set_title(title)
    ax.set_axis_off()
    ax.set_aspect('equal')


if __name__ == '__main__':
    g = gen()
    fix_outer_cycle_pos(g, get_cycle(g, 3))
    fix_all_pos(g)

    vc = min_weighted_vertex_cover(g)
    m = min_maximal_matching(g)
    print m

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))
    draw(g, ax1, 'vertex cover', vl=list(vc))
    draw(g, ax2, 'matching', el=list(m))

    plt.tight_layout()
    plt.show()
