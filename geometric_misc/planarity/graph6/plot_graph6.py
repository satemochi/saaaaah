from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms.planarity import check_planarity
import numpy as np

def get_square(n):
    for i in xrange(10000):
        if n < i * i:
            return i

def get_tutte_pos(g, embed):
    c = outer_face(g, embed)
    fix_outer_cycle_pos(g, c)
    return fix_all_pos(g)

def outer_face(g, pe):
    max_length = []
    for u, v in g.edges(): 
        c = pe.traverse_face(u, v)
        if len(c) > len(max_length):
            max_length = c 
    return max_length

def fix_outer_cycle_pos(g, cycle_vertices):
    rad = 2 * np.pi / len(cycle_vertices)
    for i, v in enumerate(cycle_vertices):
        g.node[v]['coord'] = (np.cos(rad * i), np.sin(rad * i))

def fix_all_pos(g):
    # building coefficient-matrices for xy-coordinates of the unfixed vertices
    A, Bx, By = [], [], []
    for v in g.nodes():
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
    return {v: np.array(c) for v, c in enumerate(zip(xcoords, ycoords))}


def get_pos(g, N, i):
    is_planar, certificate = check_planarity(g, counterexample=True)
    pos = get_tutte_pos(g, certificate)
    scale_factor = 1.0 / N
    t = np.array([i % N, i // N]) * scale_factor
    pos = {v: 0.35 * scale_factor * p + t for v, p in pos.items()}
    return pos

if __name__ == '__main__':
    plt.figure(figsize=(11, 11))
    """ We can refer graph data in
        https://users.cecs.anu.edu.au/~bdm/data/graphs.html
    """
#    with open('planar_conn.3.g6', 'rb') as f:
#    with open('planar_conn.4.g6', 'rb') as f:
    with open('planar_conn.5.g6', 'rb') as f:
#    with open('planar_conn.6.g6', 'rb') as f:
#    with open('planar_conn.7.g6', 'rb') as f:
#    with open('planar_conn.8.g6', 'rb') as f:
        lines = f.readlines()

    n = len(lines)
    N = get_square(n)
    print n, N
    for i, gcode in enumerate(lines):
        g = nx.from_graph6_bytes(gcode.rstrip('\n'))
        pos = get_pos(g, N, i)
        nx.draw_networkx(g, pos, node_size=0, width=0.6, with_labels=False)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig('connected_planar_graphs_n_vertices.png', bbox_inches='tight')
    plt.show()
