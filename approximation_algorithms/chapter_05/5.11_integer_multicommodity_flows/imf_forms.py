import matplotlib.pyplot as plt

def form(i):
    delta = 1.2
    fs = 13
    space = 10

    objective = r'$\min \ \ W$'
    plt.text(-1.0, i, objective, fontsize=fs)

    subjects = r'$\sum_{P: e \in P} x_P \leq W,$'
    plt.text(0.5, i - delta * 1, subjects, fontsize=fs)
    subjects = r'$e\in E,$'
    plt.text(0.5 + space, i - delta * 1, subjects, fontsize=fs)

    subjects = r'$\sum_{P\in\mathcal{P}_i} x_P = 1,$'
    plt.text(0.7, i - delta * 2, subjects, fontsize=fs, color='g')
    subjects = r'$i = 0, \ldots k - 1,$'
    plt.text(0.5 + space, i - delta * 2, subjects, fontsize=fs)

    subjects = r'$x_P \in \{0, 1\}.$'
    plt.text(0.5, i - delta * 3, subjects, fontsize=fs)
    subjects = r'$\forall P \in \mathcal{P}_i,\ \ i = 0, \ldots, k - 1$'
    plt.text(0.5 + space, i - delta * 3, subjects, fontsize=fs)


def form2(i):
    delta = 1.2
    fs = 13
    space = 12

    objective = r'$\min \ \ k|E|W + \sum_{i=0}^{k-1} u_k$'
    plt.text(-1.0, i, objective, fontsize=fs)

    subjects = r'$\sum_{i=0}^{k-1} \left(x_{uv}^i + x_{vu}^i \right) \leq W,$'
    plt.text(1.0, i - delta, subjects, fontsize=fs)
    subjects = r'$\forall(u, v) \in E$'
    plt.text(0.5 + space, i - delta, subjects, fontsize=fs)

    subjects = r'$\sum_{(s_i, v) \in E} \left(x_{s_iv}^i-x_{vs_i}^i \right)=1,$'
    plt.text(0.5, i - delta * 2, subjects, fontsize=fs, color='g')
    subjects = '$i = 0, \ldots, k - 1$'
    plt.text(0.5 + space, i - delta * 2, subjects, fontsize=fs)

    subjects = r'$\sum_{(t_i,v)\in E} \left(x_{t_iv}^i-x_{vt_i}^i \right)=-1,$'
    plt.text(0.5, i - delta * 3, subjects, fontsize=fs, color='g')
    subjects = '$i = 0, \ldots, k - 1$'
    plt.text(0.5 + space, i - delta * 3, subjects, fontsize=fs)

    subjects = r'$\sum_{(u,v)\in E:u \in V-\{s_i,t_i\}}(x_{uv}^i-x_{vu}^i)=0,$'
    plt.text(-1.5, i - delta * 4, subjects, fontsize=fs, color='g')
    subjects = r'$i=0, \ldots, k-1$'
    plt.text(0.5 + space, i - delta * 4, subjects, fontsize=fs)

    subjects = r'$\sum_{(u,v) \in E} x_{uv}^i  \leq u_i,$'
    plt.text(0.5, i - delta * 5, subjects, fontsize=fs, color='g')
    subjects = r'$i=0, \ldots, k-1$'
    plt.text(0.5 + space, i - delta * 5, subjects, fontsize=fs)

    subjects = r'$\forall x_{uv}^i \in \{0, 1\}.$'
    plt.text(0.5, i - delta * 6, subjects, fontsize=fs)

if __name__ == '__main__':
    plt.figure(figsize=(6, 6))
    form(11)
    form2(5)
    plt.title('An integer program for Integer Multicommodity flows',
              weight='bold')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-2, 12])
    plt.gca().margins(0.1)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("imf_forms.png", bbox_inches='tight')
    plt.show()
