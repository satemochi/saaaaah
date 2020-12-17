from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


class hadamard_matrix:
    """ Due to Sylvester's construction """

    def __init__(self, order):
        assert(order > 0 and self.__popcount(order) == 1)
        self.__m = self.__create(order)
        assert(self.__assert())
        from pprint import pprint
        pprint(self.__m)

    @staticmethod
    def __popcount(x):
        return bin(x).count('1')

    def __create(self, order):
        m, dim = [[1]], 1
        while dim < order:
            m = self.__extend(m)
            dim <<= 1
        return m

    @staticmethod
    def __extend(m):
        h = []
        for i in range(len(m)):
            h += [m[i]+m[i]]
        for i in range(len(m)):
            h += [m[i]+[-x for x in m[i]]]
        return h

    def __assert(self):
        from itertools import combinations
        o = len(self.__m)
        return all(sum(self.__m[i][k] * self.__m[j][k] for k in range(o)) == 0
                   for i, j in combinations(range(o), 2))

    def draw(self):
        o = len(self.__m)
        for i in range(o):
            for j in range(o):
                c = 'k' if self.__m[i][j] > 0 else 'w'
                plt.gca().add_patch(Rectangle((i, o-j-1), 1, 1, fc=c, fill=1))


if __name__ == '__main__':
    o = 1 << 3
    hadamard_matrix(o).draw()

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(0, o)
    plt.gca().set_ylim(0, o)
    plt.tight_layout()
    # plt.savefig('hadamard_matrix_01.png', bbox_inches='tight')
    plt.show()
