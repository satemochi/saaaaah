from functools import reduce
from random import shuffle
#from subprocess import run
from matplotlib import pyplot as plt
import networkx as nx
from numpy.random import geometric


def conf_model(n, p):
    shuffle(stubs := reduce(lambda x, i: x+[i]*geometric(p), range(n), []))
    return nx.MultiGraph(zip(stubs[::2], stubs[1::2]))


def prop(g):
    print('selfloop exists' if has_selfloop(g) else 'no selfloop')
    print('multiedge exists' if has_multiedge(g) else 'no multiedge')
    print('connected' if nx.number_connected_components(g) == 1
          else 'disconnected')


def has_selfloop(g):
    return any(v in list(g[v]) for v in g)


def has_multiedge(g):
    return any(i > 0 for _, _, i in g.edges)


if __name__ == '__main__':
    g = conf_model(50, 0.3)
    prop(g)

    nx.nx_agraph.to_agraph(g).draw('conf_model_ex01.png', prog='dot')
    #run('open conf_model_ex01.pdf', shell=True)

    deg_seq = list(dict(g.degree).values())
    plt.gca().set_xticks(range(max(deg_seq)))
    plt.hist(deg_seq, bins=max(deg_seq)-1, rwidth=0.8, align='left')
    plt.savefig('conf_model_ex01_deg_histogram.png', bbox_inches='tight')
    #run('open conf_model_ex01_deg_histogram.png', shell=True)
