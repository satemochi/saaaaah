import networkx as nx
from matplotlib import pyplot as plt
from itertools import izip
import math
import random
import numpy as np
import os
import subprocess


def gen():
    #    return nx.bull_graph()              # 1-connected planar
    #    return nx.chvatal_graph()           # 4-connected non-planar
    #    return nx.cubical_graph()           # 3-connected planar
    #    return nx.desargues_graph()         # 3-connected non-planar
    #    return nx.diamond_graph()           # 2-connected planar
    #    return nx.dodecahedral_graph()      # 3-connected planar
        return nx.frucht_graph()            # 3-connected planar
    #    return nx.heawood_graph()           # 3-connected planar
    #    return nx.house_graph()             # 2-connected planar
    #    return nx.house_x_graph()           # 2-connected planar
    #    return nx.icosahedral_graph()       # 5-connected planar
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
    return k == 3


def get_cycle(g, mi=None):
    # find any cycles
    cb = nx.cycle_basis(g)

    # choose longest one
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


def draw(g, pos, alpha=0.125):
    nx.draw_networkx(g, pos=pos, node_color='g', alpha=alpha,
                     with_labels=False, node_size=30)


def draw_base(g, pos1, pos2):
    draw(g, pos1)
    draw(g, pos2)


def move(g, pos1, pos2):
    src = np.array(pos1.values())
    dst = np.array(pos2.values())
    noise = np.random.normal(0, 0.75, (len(src), 2))
    files = []
    for i, t in enumerate(np.linspace(0, 1, 100)):
        plt.cla()
        draw_base(g, pos1, pos2)
        interpolate = (1-t)*src + t*dst + t*(1-t)*noise
        ipos = {i: interpolate[i] for i in range(len(interpolate))}
        plt.gca().set_axis_off()
        plt.gca().set_aspect('equal')
        plt.gca().set_xlim([-1.1, 3.6])
        plt.gca().set_ylim([-1.1, 1.1])
        draw(g, ipos, 1.0)
        plt.savefig(str(i).zfill(4) + '.png', bbox_inches='tight')
        files.append(str(i).zfill(4) + '.png')
        plt.pause(0.5)
    cmd = 'convert -layers optimize -loop 0 -delay 3 0*.png tutte_anim.gif'
    subprocess.call(cmd, shell=True)
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    g = gen()
    cycle = get_cycle(g, 2)
    fix_outer_cycle_pos(g, cycle)
    fix_all_pos(g)
    pos1 = nx.get_node_attributes(g, 'coord')

    g = gen()
    cycle = get_cycle(g, 1)
    fix_outer_cycle_pos(g, cycle)
    fix_all_pos(g)
    pos2 = {}
    for k, v in nx.get_node_attributes(g, 'coord').iteritems():
        pos2[k] = (v[0] + 2.5, v[1])

    move(g, pos1, pos2)
    plt.close()
