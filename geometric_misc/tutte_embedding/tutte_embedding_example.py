import networkx as nx
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
    return nx.icosahedral_graph()       # 5-connected planar
#    return nx.krackhardt_kite_graph()   # 1-connected planar
#    return nx.moebius_kantor_graph()    # non-planar
#    return nx.octahedral_graph()        # 4-connected planar
#    return nx.pappus_graph()            # 3-connected non-planar
#    return nx.petersen_graph()          # 3-connected non-planar
#    return nx.sedgewick_maze_graph()    # 1-connected planar
#    return nx.tetrahedral_graph()       # 3-connected planar
#    return nx.truncated_cube_graph()    # 3-connected planar
#    return nx.truncated_tetrahedron_graph() # 3-connected planar
#    return nx.tutte_graph()             # 3-connected planar


def check_connectivity(g):
    # we are allowed to any input graph be triconnected.
    k = nx.node_connectivity(g)
    print k
#    return  k < 4
    return  k == 3


def draw(g, pos=None):
    if not pos:
        pos = nx.nx_pydot.graphviz_layout(g, prog='neato')
    nx.draw_networkx(g, pos=pos, node_color='g',
                     with_labels=False, node_size=30)
    plt.axis('equal')
    plt.savefig('tutte_embedding.png', bbox_inches='tight')


def get_cycle(g):
    # find any cycles
    cb = nx.cycle_basis(g)

    # choose longest one
    argmax = lambda array: max(izip(array, xrange(len(array))))[1]
    mi = argmax([len(c) for c in cb])
#    mi = 2     # for truncated_tetrahedron
#    mi = 3      # for truncated_cube
#    mi = 6
    mi = 0      # for icosahedral

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
        a[v] = 1
        bx, by = 0, 0
        if 'coord' in g.node[v]:    # a fixed vertex which is constant
            bx = g.node[v]['coord'][0]
            by = g.node[v]['coord'][1]
        else:
            coeff = 1.0 / len(g[v])
            for n in g[v]:      # for neighbors
                a[n] = -coeff   # to be the barycenter constraint
        A.append(a)
        Bx.append(bx)
        By.append(by)
    # solving systems of linear equations
    xcoords = np.linalg.solve(A, Bx)
    ycoords = np.linalg.solve(A, By)
    # asigning coordinates
    for v, coord in enumerate(zip(xcoords, ycoords)):
        g.node[v]['coord'] = coord


if __name__ == '__main__':
    g = gen()
#    assert check_connectivity(g)
    check_connectivity(g)

    cycle = get_cycle(g)
    fix_outer_cycle_pos(g, cycle)
    fix_all_pos(g)

    draw(g, nx.get_node_attributes(g, 'coord'))
    plt.show()
