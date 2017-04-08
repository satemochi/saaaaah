import matplotlib.pyplot as plt


def form(i):
    delta = 1.0
    fs = 12
    space = 7

    title = "Lemma 5.26:"
    plt.text(-1.0, i, title, fontsize=13, weight='bold')

    statement = "For $0 \leq \delta \leq 1,$ we have that"
    plt.text(0.0, i-delta, statement, fontsize=fs)

    statement = r'$\left(\frac{e^\delta}{(1+\delta)^{(1+\delta)}}\right)^U'
    statement += r'\leq e^{-U\delta^2 /3}$'
    plt.text(space, i-delta*2, statement, fontsize=15)

    statement = "and for  $0 \leq \delta < 1,$ we have that"
    plt.text(0.0, i-delta*3, statement, fontsize=fs)

    statement = r'$\left(\frac{e^{-\delta}}{(1-\delta)^{(1-\delta)}}\right)^L'
    statement += r'\leq e^{-L\delta^2 /2}.$'
    plt.text(space, i-delta*4, statement, fontsize=15)


if __name__ == '__main__':
    plt.gcf().set_figheight(3)
    form(5)
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([0.0, 6])
    plt.axis('off')
    plt.tight_layout()
#    plt.gca().margins(0.1)
    plt.savefig("lemma5.26.png", bbox_inches='tight')
#    plt.show()
