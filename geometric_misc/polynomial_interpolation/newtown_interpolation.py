import numpy as np


def newton(xdata, ydata, sep=101):
    """ Retern the Newton interpolation polynomial evaluated in x.
            This code is an copy originating from Andre Massing.
            (see https://wiki.math.ntnu.no/tma4125/2021v/lectures)
    """
    x, F = np.linspace(xdata[0], xdata[-1], sep), __divdiff(xdata, ydata)
    xpoly, newton_poly = np.ones(sep), F[0, 0] * np.ones(len(x))
    for j in range(len(xdata)-1):
        xpoly *= x - xdata[j]
        newton_poly += (F[0, j+1] * xpoly)
    return x, newton_poly


def __divdiff(xdata, ydata):
    """ Create the table of divided differeces based on xdata and ydata. """
    F = np.zeros(((n:=len(xdata)), n))
    F[:,0] = ydata
    for j in range(n):
        for i in range(n-j-1):
            F[i, j+1] = (F[i+1, j] - F[i, j]) / (xdata[i+j+1] - xdata[i])
    return F


if __name__ == '__main__':
    xdata = [0, 1, 3]
    ydata = [3, 8, 6]
#    xdata = [1976, 1981, 1986, 1991, 1996, 2001]
#    ydata = [4017101, 4092340, 4159187, 4249830, 4369957, 4503436]
#    x, y = lagrange(xdata, ydata)

    x, y = newton(xdata, ydata)

    # import matplotlib
    from matplotlib import pyplot as plt
    # matplotlib.use('module://backend_ipe')
    plt.plot(x, y)
    plt.plot(xdata, ydata, 'o')
    plt.tight_layout()
    plt.show()
    # plt.savefig('norway_population.ipe', format='ipe')
