import picos as pic
import networkx as nx
import cvxopt as cvx
import cvxopt.lapack
import numpy as np
import matplotlib.pyplot as plt


def gen():
    G = nx.LCF_graph(20, [1, 3, 14], 5)
    for i, j in G.edges():
        G[i][j]['weight'] = 2
    return G


def random_projection(V, L, Zvp):
    # random projection algorithm
    # Repeat 100 times or until we are within a factor .878 of
    # the SDP optimal value Zvp
    count, obj, lobo = 0, 0, .878 * Zvp
    while (count < 100 or obj < lobo):
        r = cvx.normal(V.size[0])
        x = cvx.matrix(np.sign(V * r))
        o = (x.T * L * x).value[0]
        if o > obj:
            x_cut = x
            obj = o
        count += 1
    return x_cut


def unified(V):
    # Cholesky factorization
    cvxopt.lapack.potrf(V)
    for i in range(V.size[0]):
        for j in range(i + 1, V.size[0]):
            V[i, j] = 0
    return V


def cut(G):
    N = len(G.nodes())
    maxcut = pic.Problem()
    X = maxcut.add_variable('X', (N, N), 'symmetric')

    # objective
    L = pic.new_param('L', 1/4. * nx.laplacian_matrix(G).toarray())
    maxcut.set_objective('max', L | X)

    # constraints
    maxcut.add_constraint(pic.tools.diag_vect(X) == 1)
    maxcut.add_constraint(X >> 0)

    maxcut.solve(verbose=0)
    return random_projection(unified(X.value), L, maxcut.obj_value())


def draw(G, x_cut):
    # a Layout for which the graph is planar
    # (or use pos=nx.spring_layout(G) with another graph)
    pos = {0: (0.07, 0.7), 1: (0.18, 0.78), 2: (0.26, 0.45),
           3: (0.27, 0.66), 4: (0.42, 0.79), 5: (0.56, 0.95),
           6: (0.6,  0.8), 7: (0.64, 0.65), 8: (0.55, 0.37),
           9: (0.65, 0.3), 10: (0.77, 0.46), 11: (0.83, 0.66),
           12: (0.90, 0.41), 13: (0.70, 0.1), 14: (0.56, 0.16),
           15: (0.40, 0.17), 16: (0.28, 0.05), 17: (0.03, 0.38),
           18: (0.01, 0.66), 19: (0, 0.95)}

    node_colors = ['#ffcccc' if x_cut[n] < 0 else '#ffddaa'
                   for n in range(len(G.nodes()))]
    cut = [(i, j) for i, j in G.edges() if x_cut[i] * x_cut[j] < 0]

    nx.draw_networkx(G, pos, node_color=node_colors, edge_color='#999999')
    nx.draw_networkx_edges(G, pos, edgelist=cut, edge_color='#006600', width=2)

    plt.axis('off')
    plt.tight_layout()


if __name__ == '__main__':
    G = gen()
    draw(G, cut(G))
    plt.savefig('max_cut_sdp_relaxation-01.png', bbox_inches='tight')
    plt.show()
