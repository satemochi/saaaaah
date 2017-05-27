import math
import networkx as nx
import numpy as np


def __fix_outer_cycle_pos(g, cycle_vertices):
    rad = 2 * math.pi / len(cycle_vertices)
    for i, v in enumerate(cycle_vertices):
        g.node[v]['coord'] = (math.cos(rad * i), math.sin(rad * i))


def __fix_all_pos(g):
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
            a[v] = len(g[v])    #
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


def tutte_pos(g, i=0):
    pos = []
    cycles = nx.cycle_basis(g)
    if i >= len(cycles):
        i = 0
    c = cycles[i]
    __fix_outer_cycle_pos(g, c)
    __fix_all_pos(g)
    return nx.get_node_attributes(g, 'coord')

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    g = nx.frucht_graph()
    nx.draw_networkx(g, pos=tutte_pos(g))
    plt.show()


