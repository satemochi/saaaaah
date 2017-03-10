import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc


def get_closest_pair(P):
    closest_pair, d = (0, 1), np.linalg.norm(P[0] - P[1])
    for i, j in itertools.combinations(range(len(P)), 2):
        if d > np.linalg.norm(P[i] - P[j]):
            d = np.linalg.norm(P[i] - P[j])
            closest_pair = (i, j)
    return closest_pair


def get_nearest_addition_tour(P):
    S = range(len(P))
    i, j = get_closest_pair(P)
    del S[j]
    del S[i]
    tour = [i, j, i]
    while len(S) > 0:
        min_sid, correspond_tid = 0, 0
        mind = np.linalg.norm(P[S[0]] - P[tour[0]])
        for si, tj in itertools.product(range(len(S)), range(len(tour) - 1)):
            if mind > np.linalg.norm(P[S[si]] - P[tour[tj]]):
                mind = np.linalg.norm(P[S[si]] - P[tour[tj]])
                min_sid = si
                correspond_tid = tj
        tour.insert(correspond_tid + 1, S[min_sid])
        del S[min_sid]
    return tour


def draw_tour(P):
    plt.gca().scatter(P[:, 0], P[:, 1], color='r')
    tour = get_nearest_addition_tour(P)
    lines = [[P[u], P[v]] for u, v in zip(tour[:-1], tour[1:])]
    plt.gca().add_collection(mc.LineCollection(lines, colors='g',
                                               linewidth=3, zorder=-1))

if __name__ == '__main__':
    P = np.random.random((30, 2))
    draw_tour(P)
    plt.show()
