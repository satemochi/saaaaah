import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 6, 0.05)
print x
ave = [3/4.] * len(x)
rr = 1 - (1 - 1/x)**x
simple = 1 - 0.5**x

plt.plot(x, ave, label='average')
plt.plot(x, rr, label='randomized rounding')
plt.plot(x, simple, label='flipping coints')
plt.plot(x, 0.5 * (rr + simple), label='expected choosing the better')
plt.legend()

plt.savefig('5.5_plot.png', bbox_inches='tight')
plt.show()
