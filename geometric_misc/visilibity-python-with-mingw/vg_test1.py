import itertools
import matplotlib.pylab as plt
import matplotlib.collections as mc
import visilibity as vis


def draw_env(wall_choords, holes_choords):
    plt.plot([x for x, y in wall_choords] + [0],
             [y for x, y in wall_choords] + [0], 'black', alpha=0.125)
    for h in holes_choords:
        plt.gca().add_patch(plt.Polygon(h, fc='r', alpha=0.25))


def environments(epsilon=0.0000001):
    wall_choords = [(0, 0), (700, 0), (700, 900), (0, 900)]
    wall = vis.Polygon([vis.Point(x, y) for x, y in wall_choords])
    holes_choords = [[(100, 300), (100, 500), (150, 500), (150, 300)],
                     [(300, 300), (300, 500), (400, 550), (400, 300)],
                     [(90, 700), (250, 750), (220, 600), (150, 600)],
                     [(330, 700), (330, 800), (530, 850), (530, 790)],
                     [(230, 50), (250, 90), (390, 90), (390, 50)]]
    holes = []
    for hc in holes_choords:
        holes.append(vis.Polygon([vis.Point(x, y) for x, y in hc]))

    draw_env(wall_choords, holes_choords)
    env = vis.Environment([wall] + holes)
    return env, vis.Visibility_Graph(env, epsilon)


def draw_edges(env, vg):
    edges = []
    for i, j in itertools.combinations(range(vg.n()), 2):
        if vg(i, j):
            edges.append([[env(i).x(), env(i).y()], [env(j).x(), env(j).y()]])
    plt.gca().add_collection(mc.LineCollection(edges, color='g'))
    print len(edges)


if __name__ == "__main__":
    env, vg = environments()
    draw_edges(env, vg)
    plt.gca().margins(0.03)
    plt.savefig('visibility_graph_test.png')
    plt.show()
