import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-1, 1.01, 0.01)
acos = np.arccos(np.around(x, 3)) / np.pi
low = (1 - x) / 2.0
ratii = acos / low

plt.plot(x, acos, label=r'$\frac{\arccos(x)}{\pi}$')
plt.plot(x, low, label=r'$\frac{1-x}{2}$')
plt.plot(x, ratii, label=r'ratio = $\frac{2 \arccos(x)}{\pi(1-x)}$')
plt.plot(x, [0.878] * len(x), label='0.878')
plt.legend()

plt.gca().set_ylim([0, 1])
plt.savefig('6.2_plot.png', bbox_inches='tight')
plt.show()
