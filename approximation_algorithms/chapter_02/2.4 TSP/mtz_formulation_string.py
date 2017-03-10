import matplotlib.pyplot as plt


objective = r'$\min \ \ \sum_{i=0}^{n-1} \ \ \sum_{j=0}^{n-1} c_{ij} x_{ij}$' 
plt.text(0.0, 3.0, objective, fontsize=12)

incoming = r'$\sum_{i = 0, i \neq j}^{n - 1} \ x_{ij} = 1$'
plt.text(0.0, 2.0, incoming, fontsize=12)
suffix = r'$j = 0, \ldots, n - 1$'
plt.text(10.0, 2.0, suffix, fontsize=12)

outgoing = r'$\sum_{j = 0, j \neq i}^{n - 1} \ x_{ij} = 1$' 
plt.text(0.0, 1.0, outgoing, fontsize=12)
suffix = r'$i = 0, \ldots, n - 1$'
plt.text(10.0, 1.0, suffix, fontsize=12)

subtour = r'$u_i - u_j + n\ x_{ij} \leq n - 1$' 
plt.text(0.0, 0.0, subtour, fontsize=12)
suffix = r'$1 \leq i \neq j \leq n - 1$'
plt.text(10.0, 0.0, suffix, fontsize=12)

others = r'$0 \leq x_{ij} \leq 1, \ \ \ u_i \in \mathbb{Z}, \ \ \ u_0 = 0,'
others += r'\ \ \ \ \forall\ i,\ j\ \in \{0, \ldots, n - 1\}$'
plt.text(0.0, -1.0, others, fontsize=12)

plt.title('The Miller-Tucker-Zemlin Formulation')
plt.gca().set_xlim([-2, 20])
plt.gca().set_ylim([-2, 4])
plt.gca().margins(0.1)
plt.savefig("mtz_formulation.png", bbox_inches='tight')
plt.show()
