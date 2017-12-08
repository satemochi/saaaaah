import sys
from time import time
from matplotlib import pyplot as plt
import networkx as nx


def non_recursive_dfs(g):
    visited = [False] * nx.number_of_nodes(g)
    for v in g.nodes():
        if not visited[v]:
            yield v
            visited[v] = True
            stack = [(v, iter(g[v]))]
            while stack:
                parent, children = stack[-1]
                try:
                    child = next(children)
                    if not visited[child]:
                        yield child
                        visited[child] = True
                        stack.append((child, iter(g[child])))
                except StopIteration:
                    stack.pop()


def rdfs(g, v, visited):
    if not visited[v]:
        yield v
        visited[v] = True
        for w in iter(g[v]):
            for x in rdfs(g, w, visited):
                yield x


def recursive_dfs(g):
    visited = [False] * nx.number_of_nodes(g)
    for v in g.nodes():
        for x in rdfs(g, v, visited):
            yield x


def experiment(t=10):
    N = range(1000, 10001, 1000)
    p = 6
    et_rec_dfs, et_non_dfs = [], []
    E = []

    for i, n in enumerate(N):
        g = nx.fast_gnp_random_graph(n, float(p) / n)
        E.append(nx.number_of_edges(g))

        start = time()
        list(recursive_dfs(g))
        et_rec_dfs.append(time() - start)

        start = time()
        list(non_recursive_dfs(g))
        et_non_dfs.append(time() - start)

    return (N, E, et_rec_dfs, et_non_dfs)


def html(n, e, rec, non, fname="result.html"):
    tags = "<html><body><table>"
    tags += "<tr><td>V</td><td>"
    tags += "</td><td>".join(str(x) for x in n) + "</td></tr>"
    tags += "<tr><td>E</td><td>"
    tags += "</td><td>".join(str(x) for x in e) + "</td></tr>"
    tags += "<tr><td>Recursive</td><td>"
    tags += "</td><td>".join("{:.3f}".format(x) for x in rec) + "</td></tr>"
    tags += "<tr><td>Non-recursive</td><td>"
    tags += "</td><td>".join("{:.3f}".format(x) for x in non) + "</td></tr>"
    tags += "</table></body></html>"
    with open(fname, 'w') as f:
        f.write(tags)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    n, e, rec, non = experiment()
#    html(n, e, rec, non)

    plt.plot(n, rec, marker='*', color='b', label='recursive', markersize=7)
    plt.plot(n, non, marker='o', color='g', label='non-recursive')
    for i, x in enumerate(n):
        plt.gca().text(x-400, 4.5, str(e[i]), color='r')

    plt.xticks(n)
    plt.legend(loc='best')
#    plt.savefig("recursive_dfs_trials.png", bbox_inches="tight")
    plt.tight_layout()
    plt.show()
