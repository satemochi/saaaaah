import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS as mcolors


def add_each_chaps(g, chapter, captions):
    c = mcolors.keys()[chapter * 6]
    for i in range(len(captions)):
        g.add_node(str(chapter + 1) + '.' + str(i + 1),
                   caption=captions[i], color=c)


def add_chapters(g):
    captions = [
            ['The whats and wys of approximation algorithms',
             'An introduction to the techniques and to linear programming:' +
             'the set cover',
             'A deterministic rounding algorithm',
             'Rounding a dual solution',
             'Constructing a dual solution: the primal-dual method',
             'A greedy algorithm',
             'A randomized rounding algorithm'],
            ['Scheduling jobs with deadlines on a single machine',
             'The $k$-center problem',
             'Scheduling jobs on identical parallel machines',
             'The traveling salesman problem',
             'Maximizing float in bank accounts',
             'Finding minimum-degree spanning trees',
             'Edge coloring'],
            ['The knapsack problem',
             'Scheduling jobs on identical parallel machines',
             'The bin-packing problem'],
            ['Minimizing the sum of completion times on a single machine',
             'Minimizing the weighted sum of completion times on ' +
             'a single machine',
             'Solving large linear programs in polynomial time via ' +
             'the ellipsoid method',
             'The prize-collecting Steiner tree problem',
             'The uncapacitated facility location problem',
             'The bin-packing problem'],
            ['Simple algorithms for MAX SAT and MAX CUT',
             'Derandomization',
             'Flipping biased coins',
             'Randomized rounding',
             'Choosing the better of two solutions',
             'Non-linear randomized rounding',
             'The prize-collecting Steiner tree problem',
             'The uncapacitated facility location problem',
             'Scheduling a single machine with release dates',
             'Chernoff bounds',
             'Integer multicommodity flows',
             'Random Sampling and coloring dense 3-colorable graphs'],
            ['A brief introduction to semidefinite programming',
             'Finding large cuts',
             'Approximating quadratic programs',
             'Finding a correlation clustering',
             'Coloring 3-colorable graphs'],
            ['The set cover problem: a review',
             'Choosing variables to increase: ' +
             'the feedback vertex set problem in undirected graphs',
             'Cleaning up the primal solution: the shortest $s$-$t$ path ' +
             'problem',
             'Increasing multiple variables at once: ' +
             'the generalized Steiner tree problem',
             'Strengthening inequalities: the minimum knapsack problem',
             'The uncapacitated facility location problem',
             'Lagrangean relaxation and the $k$-median problem'],
            ['The multiway cut problem and a minimum-cut-based algorithm',
             'The multiway cut problem and an LP rounding algorithm',
             'The multicut problem',
             'Balanced cuts',
             'Probabilistic approximation of metrics by tree metrics',
             'An application of tree metrics: Buy-at-bulk network design',
             'Spreading metrics, tree metrics, and linear arrangement'],
            ['A local search algorithm for the uncapacitated facility ' +
             'location problem',
             'A local search algorithm for the k-median problem',
             'Minimum-degree spanning trees',
             'A greedy algorithm for the uncapacitated ' +
             'facility location problem'],
            ['The Euclidean traveling salesman problem',
             'The maximum independent set problem in planar graphs'],
            ['The generalized assignment problem',
             'Minimum-cost bounded-degree spanning trees',
             'Survivable network design and iterated rounding'],
            ['The uncapacitated facility location problem',
             'The single-source rent-or-buy problem',
             'The Steiner tree problem',
             'Everything at once: finding a large cut in a dense graph'],
            ['Approximating quadratic programs',
             'Coloring 3-colorable graphs',
             'Unique games'],
            ['The prize-collecting Steiner tree problem',
             'The feedback vertex set problem in undirected graphs'],
            ['Low distortion embeddings and the sparsest cut proble',
             'Oblivious routing and cut-tree packings',
             'Cut-tree packings and the minimum bisection problem',
             'The uniform sparsest cut problem'],
            ['Reductions from NP-complete problems',
             'Reductions that preserve approximation',
             'Reductions from probabilistically checkable proofs',
             'Reductions from label cover',
             'Reductions from unique games']
    ]
    for i, c in enumerate(captions):
        add_each_chaps(g, i, c)


def add_relationships(g):
    terms = ['scheduling',              # 0
             'max sat',                 # 1
             'maximum independent set', # 2
             'vertex cover',            # 3
             'facility location',       # 4
             'unique games',            # 5
             'Steiner tree',            # 6
             'network design',          # 7
             'multicut',                # 8
             'max cut',                 # 9
             'tree metric',             # 10
             'chernoff bound',          # 11
             'sparsest cut',            # 12
             'ellipsoid method',        # 13
             'cut-tree packing',        # 14
             'minimum bisection',       # 15
             'feedback vertex set',     # 16
             'quadratic programming',   # 17
             'coloring',                # 18
             'independent set',         # 19
             'region-growing',          # 20
             'minimum spanning tree',   # 21
             'random sampling',         # 22
             'TSP',                     # 23
             'k-median',                # 24
             'k-center',                # 25
             'set cover',               # 26
             'Lagrangean multiplier',   # 27
             'complementary slackness',  # 28
             'integrality gap',         # 29
             'knapsack',                # 30
             'randomized rounding',     # 31
             'high probability',        # 32
             'PTAS',                    # 33
             'harmonic number']         # 34

    #    g.add_edge('1.4', '1.3')
    #    g.add_edge('1.5', '1.4')
    #    g.add_edge('1.5', '1.3')
    #    g.add_edge('1.7', '1.6')
    #    g.add_edge('1.7', '1.3')

    g.add_edge('2.3', '2.1', term=terms[0])

    g.add_edge('3.2', '2.3', term=terms[0])
    #    g.add_edge('3.2', '3.1')
    #    g.add_edge('3.3', '3.2')

    #    g.add_edge('4.2', '4.1')
    #    g.add_edge('4.4', '4.3')
    g.add_edge('4.4', '1.3', term=terms[26])
    g.add_edge('4.6', '3.3', term=terms[33])
    g.add_edge('4.6', '4.3', term=terms[13])
    g.add_edge('4.6', '3.1', term=terms[30])
    g.add_edge('4.6', '1.6', term=terms[34])

    #    g.add_edge('5.2', '5.1')
    #    g.add_edge('5.4', '5.3')
    g.add_edge('5.4', '1.7', term=terms[9])
    #    g.add_edge('5.5', '5.4')
    #    g.add_edge('5.5', '5.1')
    g.add_edge('5.7', '4.4', term=terms[6])
    #    g.add_edge('5.7', '5.6')
    g.add_edge('5.8', '4.5', term=terms[4])
    g.add_edge('5.9', '4.2', term=terms[0])
    g.add_edge('5.9', '4.1', term=terms[0])
    g.add_edge('5.11', '1.7', term=terms[32])

    g.add_edge('6.2', '5.1', term=terms[9])
    #    g.add_edge('6.3', '6.2')
    #    g.add_edge('6.4', '6.3')
    #    g.add_edge('6.4', '6.2')
    g.add_edge('6.5', '5.12', term=terms[18])
    g.add_edge('6.5', '6.4')

    g.add_edge('7.1', '1.5', term=terms[26])
    g.add_edge('7.1', '1.4', term=terms[28])
    g.add_edge('7.1', '5.6', term=terms[29])
    #    g.add_edge('7.3', '7.2')
    #    g.add_edge('7.4', '7.3')
    g.add_edge('7.4', '5.7', term=terms[6])
    g.add_edge('7.5', '3.1', term=terms[30])
    g.add_edge('7.6', '4.5', term=terms[4])
    g.add_edge('7.6', '5.8', term=terms[4])
    #    g.add_edge('7.6', '7.5')
    g.add_edge('7.7', '2.2', term=terms[25])
    g.add_edge('7.7', '4.5', term=terms[4])

    g.add_edge('8.3', '4.3', term=terms[13])
    #    g.add_edge('8.4', '8.3')
    g.add_edge('8.4', '4.3', term=terms[13])
    #    g.add_edge('8.6', '8.5')
    #    g.add_edge('8.7', '8.5')
    g.add_edge('8.7', '4.3', term=terms[13])

    g.add_edge('9.1', '7.6', term=terms[4])
    g.add_edge('9.2', '7.7', term=terms[24])
    g.add_edge('9.2', '2.2', term=terms[25])
    #    g.add_edge('9.2', '9.1')
    g.add_edge('9.3', '2.6', term=terms[21])
    g.add_edge('9.4', '1.6', term=terms[26])
    g.add_edge('9.4', '4.5', term=terms[4])
    g.add_edge('9.4', '7.6', term=terms[4])
    g.add_edge('9.4', '7.7', term=terms[27])
    #    g.add_edge('9.4', '9.1')

    g.add_edge('10.1', '2.4', term=terms[23])

    g.add_edge('11.2', '2.6', term=terms[21])
    g.add_edge('11.2', '9.3', term=terms[21])
    g.add_edge('11.2', '4.3', term=terms[13])
    g.add_edge('11.3', '7.4', term=terms[6])
    g.add_edge('11.3', '4.3', term=terms[13])
    # g.add_edge('11.3', '11.2')

    g.add_edge('12.1', '4.5', term=terms[4])
    g.add_edge('12.1', '5.8', term=terms[4])
    g.add_edge('12.2', '2.4', term=terms[21])
    g.add_edge('12.3', '7.4', term=terms[6])
    g.add_edge('12.4', '5.1', term=terms[9])
    g.add_edge('12.4', '5.12', term=terms[22])

    g.add_edge('13.1', '6.3', term=terms[17])
    g.add_edge('13.2', '6.5', term=terms[18])
    g.add_edge('13.2', '10.2', term=terms[19])
    # g.add_edge('13.2', '13.1')
    g.add_edge('13.3', '5.1', term=terms[9])
    g.add_edge('13.3', '6.2', term=terms[9])
    g.add_edge('13.3', '12.4', term=terms[9])
    g.add_edge('13.3', '8.3', term=terms[20])
    g.add_edge('13.3', '8.4', term=terms[20])

    g.add_edge('14.1', '4.4', term=terms[6])
    g.add_edge('14.1', '5.7', term=terms[6])
    g.add_edge('14.1', '7.3', term=terms[6])
    g.add_edge('14.1', '7.4', term=terms[6])
    g.add_edge('14.2', '7.2', term=terms[16])
    g.add_edge('14.2', '7.4', term=terms[6])

    g.add_edge('15.1', '8.5', term=terms[10])
    g.add_edge('15.1', '5.10', term=terms[11])
    g.add_edge('15.2', '8.7', term=terms[10])
    g.add_edge('15.2', '4.3', term=terms[13])
    g.add_edge('15.3', '15.2', term=terms[14])
    g.add_edge('15.3', '8.5', term=terms[10])
    g.add_edge('15.3', '8.4', term=terms[15])
    g.add_edge('15.4', '15.1', term=terms[12])
    g.add_edge('15.4', '8.4', term=terms[15])

    g.add_edge('16.1', '11.1', term=terms[0])
    g.add_edge('16.2', '5.1', term=terms[1])
    g.add_edge('16.2', '10.2', term=terms[2])
    g.add_edge('16.2', '1.2', term=terms[3])
    g.add_edge('16.2', '4.5', term=terms[4])
    g.add_edge('16.4', '13.3', term=terms[5])
    g.add_edge('16.4', '7.4', term=terms[6])
    g.add_edge('16.4', '11.3', term=terms[7])
    g.add_edge('16.5', '13.3', term=terms[5])
    g.add_edge('16.5', '8.3', term=terms[8])
    g.add_edge('16.5', '6.2', term=terms[9])
    # g.add_edge('16.5', '16.3')


def draw(g):
    # pos = nx.nx_pydot.graphviz_layout(g, prog='neato')
    pos = nx.nx_pydot.graphviz_layout(g, prog='dot')
    colors = [g.node[v]['color'] for v in g.nodes_iter()]
    nodelist = g.nodes()
    # nodelist = [v for v in g.nodes_iter() if g.degree(v) > 0]
    nx.draw_networkx(g, pos=pos, node_color=colors, font_size=6, alpha=0.5,
                     node_size=100, arrows=False, nodelist=nodelist)
    #                 labels=nx.get_node_attributes(g, 'caption'))

    nx.draw_networkx_edge_labels(g, pos, font_size=7,
                                 edge_labels=nx.get_edge_attributes(g, 'term'))
    plt.axis('off')
    plt.tight_layout()


if __name__ == '__main__':
    g = nx.DiGraph()
    add_chapters(g)
    add_relationships(g)
    nx.write_gml(g, 'chaps.gml')
    draw(g)
    plt.show()
