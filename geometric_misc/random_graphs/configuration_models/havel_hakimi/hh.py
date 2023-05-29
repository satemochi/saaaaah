from matplotlib import pyplot as plt
import networkx as nx


def havel_hakimi(d):
    g, t = nx.Graph(), [(di, i) for i, di in enumerate(d)]
    for i in range(len(d)-1):
        t.sort()
        deg, i = t[-1]
        if deg < 1:
            break
        tt = [(di-1, _) for di, _ in t[-deg-1:-1]]
        if any(di < 0 for di, _ in tt):
            return False
        g.add_edges_from([(i, j) for _, j in t[-deg-1:-1]])
        t = t[:-deg-1] + tt
    return g


if __name__ == '__main__':
    d = [5, 5, 3, 3, 2, 2, 2]
#    d = [5, 5, 5, 5, 2, 2, 2]      # non-graphic
    x = havel_hakimi(d)
    if x is False:
        print('non-graphic degree sequence...')
    else:
        print('graphic! then, ...')
        pos = nx.spring_layout(x)
        nx.draw_networkx_nodes(x, pos, node_color='#ffc800').set_edgecolor('k')
        nx.draw_networkx_edges(x, pos)
        nx.draw_networkx_labels(x, pos)
        plt.gca().set_title(f'Given degree sequence: {d}')
        plt.gca().set_aspect('equal')
        plt.gca().axis('off')
        plt.tight_layout()
        # plt.savefig('havel_hakimi_01.png', bbox_inches='tight')
        plt.show()
