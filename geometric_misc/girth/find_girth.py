from collections import deque
import math
import networkx as nx


def get_children(g, root, level):
    return [c for c in g[root] if level[c] < 0]


def bfs_girth(g, root, girth=math.inf):
    level = {x: -1 for x in g}
    level[root] = 0
    stop_level = (girth - 1) // 2 - 1 if math.isfinite(girth) else math.inf
    bfs_stack = deque([(root, get_children(g, root, level))])

    while bfs_stack:
        x, children = bfs_stack.popleft()
        cl = math.inf
        for y in children:
            if level[y] < 0:
                level[y] = level[x] + 1
                if level[x] < stop_level:
                    bfs_stack.append((y, get_children(g, y, level)))
            else:
                c = level[x] + level[y] + 1
                if c < cl:
                    cl = c
                    if level[x] == level[y]:
                        break
        if cl < girth:
            girth = cl
            break
    return girth


def find_girth(g):
    girth = math.inf
    for v in g:
        cg = bfs_girth(g, v, girth)
        if cg < girth:
            girth = cg
        if girth == 3:
            break
    return girth


if __name__ == '__main__':
#    g = nx.chvatal_graph()     # 4
#    g = nx.frucht_graph()      # 3
#    g = nx.petersen_graph()    # 5
#    g = nx.desargues_graph()   # 6
    g = nx.heawood_graph()   # 6
    print(find_girth(g))
