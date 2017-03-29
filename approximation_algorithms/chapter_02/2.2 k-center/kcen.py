import numpy as np
import matplotlib.pyplot as plt


def gen(n=2, k=3):
    P = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
    for i in range(k - 1):
        pts = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
        P = np.concatenate((P, pts))
    return P


def greedy_2_approx(V, k):
    S = [np.random.randint(len(V))]
    while len(S) < k:
        dists = []
        for i in range(len(V)):
            dists.append(min(np.linalg.norm(V[i] - V[s]) for s in S))
        S.append(np.argmax(dists))
    return S


def radius(V, S):
    return max(min(np.linalg.norm(V[i] - V[s]) for s in S)
               for i in range(len(V)))


def draw_circle(V, S, r):
    for s in S:
        c = plt.Circle(V[s], r, alpha=0.125, color='g', edgecolor=None)
        plt.gca().add_artist(c)
    plt.gca().scatter(V[S, 0], V[S, 1], color='r', s=10)
    print r


def draw(V, S):
    plt.gca().scatter(V[:, 0], V[:, 1], s=10)
    draw_circle(V, S, radius(V, S))

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.gca().set_xlim([-1, 11])
    plt.gca().set_ylim([-1, 11])


if __name__ == '__main__':
    n, k = 15, 9
    V = gen(n, k * 1)
    S = greedy_2_approx(V, k)
    draw(V, S)
    plt.savefig('kcen.png', bbox_inches='tight')
    plt.show()
