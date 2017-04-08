import matplotlib.pyplot as plt


def form(i):
    delta = 0.7
    fs = 12
    space = 12

    title = "Theorem 5.23:"
    plt.text(-1.0, i, title, fontsize=13, weight='bold')

    statement = "Let $X_1,\ldots,X_n$ be $n$ independent 0-1 random variables,"
    plt.text(0.0, i-delta, statement, fontsize=fs)
    statement = "not necessarily identically distributed."
    plt.text(0.0, i-delta-0.5, statement, fontsize=fs)

    statement = r'Then for $X = \sum_{i=1}^n X_i$ and $\mu = E[X], '
    statement += r'L \leq \mu \leq U,$ and $\delta > 0,$'
    plt.text(0.0, i-delta*3, statement, fontsize=fs)

    state = r'Pr[$X \geq (1 + \delta) U$] $<'
    state += r'\left(\frac{e^\delta}{(1+\delta)^{(1+\delta)}}\right)^U,$'
    plt.text(3.0, i-delta*5, state, fontsize=13)

    state = r'Pr[$X \leq (1 - \delta) L$] $<'
    state += r'\left(\frac{e^{-\delta}}{(1-\delta)^{(1-\delta)}}\right)^L.$'
    plt.text(3.0, i-delta*7, state, fontsize=13)


if __name__ == '__main__':
    form(5)
    plt.title('Chernoff bounds', weight='bold')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-2.0, 6])
    plt.gca().margins(0.1)
    plt.axis('off')
    plt.savefig("chernoff_bounds.png", bbox_inches='tight')
#    plt.show()
