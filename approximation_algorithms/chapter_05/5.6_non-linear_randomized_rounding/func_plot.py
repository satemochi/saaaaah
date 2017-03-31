import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 1.01, 0.01)
up = 4**(x - 1)
low = 1 - 4**(-x)

plt.plot(x, up, label=r'$4^{x - 1}$')
plt.plot(x, low, label=r'$1 - 4^{-x}$')
plt.fill_between(x, low, up, facecolor='green', alpha=0.2, interpolate=True)
plt.legend()

plt.gca().set_xlim([0, 1])
plt.gca().set_ylim([0, 1])
plt.savefig('5.6_plot.png', bbox_inches='tight')
plt.show()
