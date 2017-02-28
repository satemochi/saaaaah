import matplotlib.pyplot as plt

s = r'Fact 1.10: '
s += ' $a_1, \ldots, a_k$ and $b_1, \ldots, b_k$ are positive numbers.'
plt.text(0.0, 1.0, s, fontsize=14)

leq = r'\ \ \ \leq \ \ \ '
math_string = r'$\min_{i = 1, \ldots, k}\ \ \frac{a_i}{b_i} ' + leq
math_string += r'\frac{\sum_{i=1}^k \ \ a_i}{\sum_{i=1}^k \ \ b_i} ' + leq
math_string += r'\max_{i = 1, \ldots, k}\ \ \frac{a_i}{b_i}$'
plt.text(0.0, 0.0, math_string, fontsize=20)

plt.gca().set_xlim([-2, 20])
plt.gca().set_ylim([-2, 3])
plt.gca().margins(0.1)
plt.savefig('fact_1.10_equations.png')
plt.show()
