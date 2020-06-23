from copy import copy
import heapq
from pprint import pprint
import random
from matplotlib import pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


def encode(d):
    plt.subplots()
    t, r = get_tree(get_heap(get_histogram(d)))
    stack, visited, code = [(r, "")], {v: False for v in t}, {c: "" for c in d}
    while stack:
        v, label = stack.pop()
        visited[v] = True
        zero, one = get_child(t, v, visited)
        proc(code, stack, zero, label+"0")
        proc(code, stack, one, label+"1")
    pprint(code)

    # pos = nx.spring_layout(t)
    # pos = graphviz_layout(t, prog='dot')
    # pos = graphviz_layout(t, prog='twopi')
    pos = hierarchy_pos(t, r)
    nx.draw_networkx_nodes(t, pos, node_color='#55aa55')
    nx.draw_networkx_edges(t, pos, alpha=0.2)
    nx.draw_networkx_nodes(t, pos, nodelist=[r], node_color='r')
    labels = {v: f'{v}:{code[v]}' if v in code else "" for v in t}
    pprint(labels)
    nx.draw_networkx_labels(t, pos, labels=labels, font_size=9,
                            font_weight='bold')
    plt.title(d)
    plt.tight_layout()
    # plt.savefig('huffman_tree.png', bbox_inches='tight')
    plt.show()


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0,
                  xcenter = 0.5):
    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    """
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos: G is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0,
                       xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                    vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent=root)
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def proc(code_table, stack, v, l):
    if v in code_table:
        code_table[v] = l
    else:
        stack.append((v, l))


def get_tree(q):
    g = nx.Graph()

    print(q)
    put_legend(q)

    while len(q) > 1:
        (ap, al), (bp, bl) = heapq.heappop(q), heapq.heappop(q)
        heapq.heappush(q, (ap+bp, al+bl))
        g.add_edges_from([(al, al+bl), (bl, al+bl)])
    return g, q[0][1]


def put_legend(q):
    c = copy(q)
    for count, char in sorted(c, key=lambda a: a[1]):
        plt.plot([0.5], [-0.05], color='white', label=f'{char}: {count}')
    plt.gca().legend(frameon=False, loc='best')


def get_child(g, v, visited):
    return [v for v in g[v] if not visited[v]]


def get_histogram(data, h={}):
    for c in data:
        h[c] = h[c] + 1 if c in h else 1
    return h


def get_heap(hist):
    q = [(v, k) for k, v in hist.items()]
    heapq.heapify(q)
    return q


if __name__ == '__main__':
    s = "Hello world."
    s = "Hello hello, hello world."
    # s = "Hello hello, hello world................"
    s = "aaabbaaacdcdaaabbbzzzz"
    print(s)
    encode(s)
