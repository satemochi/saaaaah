import matplotlib
from matplotlib import pyplot as plt
import numpy as np


def omega(xdata, x):
    # compute omega(x) for the nodes in xdata
    n1 = len(xdata)
    omega_value = np.ones(len(x))
    for j in range(n1):
        omega_value = omega_value*(x-xdata[j])  # (x-x_0)(x-x_1)...(x-x_n)
    return omega_value


if __name__ == '__main__':
    # Plot omega(x)
    a, b = -1, 1
    x = np.linspace(a, b, 501)

#    matplotlib.use('module://backend_ipe')

    plt.gca().grid(True)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$\omega(x)$')
    plt.gca().set_ylim(-1, 1)

    for n in range(1, 16):
        xdata = np.linspace(a, b, n)
        plt.plot(x, omega(xdata, x))

        plt.gca().grid(True)
#        plt.xlabel(r'$x$')
#        plt.ylabel(r'$\omega(x)$')
        plt.title(f'$n = {n}$')
        
        plt.draw()
        plt.pause(0.5)
#        plt.savefig(f'omega_{str(n).zfill(2)}.ipe', format='ipe')
        plt.cla()

        # print(f'n = {n}, max|omega(x)| = {max(abs(omega(xdata, x)))}')

    plt.tight_layout()
    plt.show()

