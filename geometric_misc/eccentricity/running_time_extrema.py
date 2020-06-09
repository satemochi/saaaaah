from time import time
import networkx as nx

""" how fast extrema_bounding """

def x(g):
    start = time()
    nx.diameter(g)
    time_diam = time() - start

    start = time()
    nx.extrema_bounding(g)
    time_ext = time() - start
    return time_diam, time_ext

if __name__ == '__main__':
    ############### tree
    g = nx.balanced_tree(4, 5)
    t1, t2 = x(g)
    print(f'diameter: {t1}, extrema_bounding: {t2}')
