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


if __name__ == '__main__':
    # xdata = [0, 1, 3]
    # ydata = [3, 8, 6]
    xdata = [1976, 1981, 1986, 1991, 1996, 2001]
    ydata = [4017101, 4092340, 4159187, 4249830, 4369957, 4503436]
    x, y = lagrange(xdata, ydata)

    # import matplotlib
    from matplotlib import pyplot as plt
    # matplotlib.use('module://backend_ipe')
    plt.plot(x, y)
    plt.plot(xdata, ydata, 'o')
    plt.tight_layout()
    plt.show()
    # plt.savefig('norway_population.ipe', format='ipe')
