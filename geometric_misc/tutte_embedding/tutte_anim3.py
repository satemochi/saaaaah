import math
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx


def gen():
    # predefined graphs in networkx
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


def get_pos():
    pos = []
    for c in nx.cycle_basis(gen()):
        g = gen()
        fix_outer_cycle_pos(g, c)
        fix_all_pos(g)
        pos.append(nx.get_node_attributes(g, 'coord'))
    pos.append(pos[0])
    return pos


def slot():
    g = gen()
    pos = get_pos()
    for s, d in zip(pos[:-1], pos[1:]):
        src = np.array(s.values())
        dst = np.array(d.values())
        noise = np.random.normal(0, 0.75, (len(src), 2))
        for t in np.linspace(0, 1, 20):
            yield (g, src, dst, noise, t)


def reset_ax():
    plt.cla()
    plt.gca().set_axis_off()
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim([-1.1, 1.1])
    plt.gca().set_ylim([-1.1, 1.1])


def draw_vertices(P):
    for p in P:
        c = plt.Circle(p, 0.02, color='g', clip_on=False)
        plt.gca().add_artist(c)


def draw_edges(g, P):
    for u, v in g.edges_iter():
        l = plt.Line2D([P[u][0], P[v][0]], [P[u][1], P[v][1]],
                       linewidth=1, color='k', alpha=0.5, zorder=-1,
                       clip_on=False)
        plt.gca().add_artist(l)


def move(slot):
    reset_ax()
    g, src, dst, noise, t = slot
    interpolate = (1-t)*src + t*dst + t*(1-t)*noise
    draw_vertices(interpolate)
    draw_edges(g, interpolate)


if __name__ == '__main__':
    save_count = len(nx.cycle_basis(gen())) * 20
    ani = FuncAnimation(plt.gcf(), move, slot, save_count=save_count)
    ani.save('e4.gif', writer='imagemagick', fps=40)
