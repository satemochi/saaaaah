from matplotlib import pyplot as plt
import numpy as np


def kaczmarz(A, b, max_iters=1000, tol=1e-12):
    x = np.zeros(A.shape[1])    # Initial guess, typically zero
    plt.scatter([x[0]], [x[1]])
    for _ in range(max_iters):
        for i in range(A.shape[0]):
            ai, bi = A[i], b[i]
            if (denom := np.dot(ai, ai)) == 0:
                continue
            _ = x
            x = x + (bi - np.dot(ai, x)) / denom * ai
            plt.scatter([x[0]], [x[1]], zorder=5)
            plt.plot([_[0], x[0]], [_[1], x[1]], c='g', alpha=0.2)
        if np.linalg.norm(b - A @ x, np.inf) / np.linalg.norm(b, np.inf) < tol:
            break
    return x


def __draw_lines(A, b, xmin=-10, xmax=10):
    x = np.array([xmin, xmax])
    for i in range(A.shape[0]):
        y = ((-A[i, 0] * x + b[i]) / A[i, 1])
        plt.plot(x, y)


if __name__ == '__main__':
    A = np.array([[3, 1], [1, 2]])
    b = np.array([9, 8])
    x, y = kaczmarz(A, b)
    print("Solution x:", kaczmarz(A, b))
    plt.scatter([x], [y], c='y', ec='k', zorder=5)

    xmin, xmax = -5, 5
    plt.gca().set_xlim(xmin, xmax)
    plt.gca().set_ylim(xmin, xmax)
    __draw_lines(A, b, xmin, xmax)

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig('kaczmarz_01.png', bbox_inches='tight')
    plt.show()
