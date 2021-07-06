from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpProblem, LpVariable, lpSum, PULP_CBC_CMD


def ipla(g):
    n, k, h = g.order(), max(deg for _, deg in g.degree), g.to_directed()

    lp = LpProblem()
    lp += (w := LpVariable('w'))

    for u in h.nodes:
        h.nodes[u]['v'] = [LpVariable(f'y{u},{i}', 1, n, 'Integer')
                           for i in range(k)]
    for u, v in g.edges:
        h[u][v]['v'] = [LpVariable(f'x{u},{v},{i}', cat='Binary')
                        for i in range(k)]
        h[v][u]['v'] = [LpVariable(f'x{v},{u},{i}', cat='Binary')
                        for i in range(k)]
        lp += lpSum(h[u][v]['v']) + lpSum(h[v][u]['v']) == 1
        lp += w >= lpSum((i + 1) * h[u][v]['v'][i] + (i + 1) * h[v][u]['v'][i]
                         for i in range(k))
        for i in range(k):
            lp += (h.nodes[u]['v'][i] - h.nodes[v]['v'][i] +
                   (n - 1) * h[u][v]['v'][i] <= n - 2)
            lp += (h.nodes[v]['v'][i] - h.nodes[u]['v'][i] +
                   (n - 1) * h[v][u]['v'][i] <= n - 2)
    for u in h.nodes:
        for i in range(k):
            lp += lpSum(h[u][v]['v'][i] for v in h.successors(u)) <= 1
            lp += lpSum(h[v][u]['v'][i] for v in h.predecessors(u)) <= 1

    PULP_CBC_CMD(msg=0).solve(lp)
    # print(w.varValue)
    # from pprint import pprint
    # for v in g:
    #     pprint([x.varValue for x in h.nodes[v]['v']])
    # for u, v in h.edges:
    #     pprint([x.varValue for x in h[u][v]['v']])
    ep = {}
    for u, v in g.edges:
        if sum((res := [h[u][v]['v'][i].varValue for i in range(k)])) != 0:
            ep[(u, v)] = res.index(1.0)
        else:
            ep[(u, v)] = [h[v][u]['v'][i].varValue for i in range(k)].index(1.0)
    return ep


def gen(d, n):
    return nx.random_regular_graph(d, n)


if __name__ == '__main__':
    g = gen(d := 4, n := 15)

    edge_partition = ipla(g)
    from pprint import pprint
    pprint(edge_partition)
    print(f'#-of linear forests: {max(i for i in edge_partition.values())+1}')

    cmap = plt.get_cmap('tab10')
    ec = [cmap(edge_partition[e]) for e in g.edges]

    pos = nx.spring_layout(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffffcc')
    nodes.set_edgecolor('black')
    nx.draw_networkx_edges(g, pos, edge_color=ec, width=2)
    nx.draw_networkx_labels(g, pos, font_size=10)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.show()
