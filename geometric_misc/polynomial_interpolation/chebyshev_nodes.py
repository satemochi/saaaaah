import numpy as np


def lagrange(xdata, ydata, sep=101):
    """ Retern the Lagrange polynomial
            This code is an copy originating from Andre Massing.
            (see https://wiki.math.ntnu.no/tma4125/2021v/lectures)
    """
    x = np.linspace(xdata[0], xdata[-1], sep)
    card_func = __cardinal(xdata, x)
    return x, sum(ydata[i] * card_func[i] for i in range(len(ydata)))


def __cardinal(xdata, x):
    card_func = []
    for i in range(n := len(xdata)):
        li = np.ones(len(x))
        for j in range(n):
            if i is not j:
                li *= (x - xdata[j]) / (xdata[i]-xdata[j])
        card_func.append(li)
    return card_func


def chebyshev_nodes(a, b, n):
    i = np.array(range(n))
    x = np.cos((2 * i + 1) * np.pi / (2 * n))
    return 0.5 * (b - a) * x + 0.5 * (b + a)


if __name__ == '__main__':
    # import matplotlib
    # matplotlib.use('module://backend_ipe')
    from matplotlib import pyplot as plt
    x = np.linspace(-1, 1, 200)
    f = 1 / (1 + 25 * x**2)

    for n in range(3, 22):
        plt.plot(x, f)

        xdata = chebyshev_nodes(-1, 1, n)
        ydata = [1 / (1 + 25 * xi**2) for xi in xdata]
        x, y = lagrange(xdata, ydata, 200)

        plt.plot(x, y)
        plt.plot(xdata, ydata, 'o')

        plt.title(f"$n = {n}$")
        plt.draw()
        plt.pause(0.5)
#        plt.savefig(f'runge_{str(n).zfill(2)}.ipe', format='ipe')
        plt.cla()
        plt.gca().set_ylim(-0.1, 1.1)

#    plt.tight_layout()
    plt.show()
    # plt.savefig('norway_population.ipe', format='ipe')
