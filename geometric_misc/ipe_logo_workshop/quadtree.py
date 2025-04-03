from matplotlib import pyplot as plt
import numpy as np


class square:
    """
    Simple square class
    """
    def __init__(self, x, y, L):
        self.x, self.y = x, y
        self.L = L

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + '),' + str(self.L)

    def containing(self, p):
        """
        Check whether it contains given point or not
        """
        return self.__xalign(p) and self.__yalign(p)

    def __xalign(self, p):
        return (self.x <= p[0]) and (p[0] <= self.x + self.L)

    def __yalign(self, p):
        return (self.y <= p[1]) and (p[1] <= self.y + self.L)

    def subsq(self):
        """
        Return the list of four children subsquares if it can be subdivisable
        """
        L = self.L >> 1
        if L == 0:
            return None
        else:
            return (square(self.x, self.y, L),
                    square(self.x + L, self.y, L),
                    square(self.x, self.y + L, L),
                    square(self.x + L, self.y + L, L))

    def plot(self):
        """
        Plot square:
            putting corners counterclockwisely from bottom-left to bottom-left
        """
        plt.plot([self.x, self.x + self.L, self.x + self.L, self.x, self.x],
                 [self.y, self.y, self.y + self.L, self.y + self.L, self.y],
                 c='k', alpha=0.25, linewidth=0.5)


class node:
    """
    Quadtree node class

    Parameters
    ----------
    qt : quadtree instance
        pointer to quadtree instance.

        we may refer to confirm properties of its quadtree configurations.

    c : list of node
        pointer to children nodes. For i = 0, 1, 2, 3, each node c[i]
        corresponds to SouthWest(SW), SouthEast(SE), NorthWest(NW), and
        NorthEast(NE) quadrants respectively.
        i.e.) [i==0 -> SW], [i==1 -> SE], [i==2 -> NW], [i==3 -> NE]

    bep : tuple of int
        pair of begin and end iterators of the list of stored points.

        On subdivision processes, we manipulate ordering of stored points
        in the SW-SE-NW-NE fashion. Then, we can refer points contained in
        this node by using slice notation.

    sq : square
        pointer to corresponding square

    h : int
        the height or level of this node. root of quad tree has level 0.

    lc : int
        location code of this node.

    a : node
        point to parent node

    """
    def __init__(self, quadtree, begin_end_pair, square, location_code,
                 height, ancestor):
        self.qt = quadtree
        self.c = [None] * 4
        self.bep = begin_end_pair
        self.sq = square
        self.h = height
        self.lc = location_code
        self.qt.loc[repr(self)] = self
        self.a = ancestor
        if self.sq.L > 1 and len(self) > self.qt.k:
            self.__subdivision()
        else:
            for p in self.qt.p[self.bep[0]:self.bep[1]]:
                self.qt.leaves[tuple(p)] = self

    def __repr__(self):
        return str(self.lc).zfill(self.h)

    def __len__(self):
        return self.bep[1] - self.bep[0]

    def __subdivision(self):
        assert(self.sq.L > 1)
        subsq = self.sq.subsq()
        beps = self.__partitioning()
        for i, be in enumerate(beps):
           if be:
                assert(all(subsq[i].containing(p)
                           for p in self.qt.p[be[0]:be[1]]))
                self.c[i] = node(self.qt, be, subsq[i],
                                 self.lc * 10 + i, self.h + 1, self)

    def __partitioning(self):
        subsets = self.__extract_subsets_with_quadrants()
        return self.__construct_begin_end_pairs(subsets)

    def __extract_subsets_with_quadrants(self):
        pts = self.qt.p[self.bep[0]:self.bep[1]]
        cx, cy = self.sq.x + (self.sq.L >> 1), self.sq.y + (self.sq.L >> 1)
        subs = []
        below, above = pts[pts[:, 1] <= cy], pts[pts[:, 1] > cy]
        subs.append(below[below[:, 0] <= cx])    # south-west
        subs.append(below[below[:, 0] > cx])     # south-east
        subs.append(above[above[:, 0] <= cx])    # north-west
        subs.append(above[above[:, 0] > cx])     # north-east
        self.__replace_points(subs)
        return subs

    def __replace_points(self, subs):
        new_pts = np.concatenate(subs, axis=0)
        head, tail = self.bep
        if head > 0:
            new_pts = np.concatenate([self.qt.p[:head], new_pts], axis=0)
        if tail < len(self.qt.p):
            new_pts = np.concatenate([new_pts, self.qt.p[tail:]], axis=0)
        assert(len(self.qt.p) == len(new_pts))
        self.qt.p = new_pts

    def __construct_begin_end_pairs(self, subs):
        head, beps = self.bep[0], []
        for s in subs:
            if len(s) > 0:
                beps.append((head, head + len(s)))
                head += len(s)
            else:
                beps.append(None)
        return beps

    def plot(self):
        self.sq.plot()
        if all(self.c[i] is None for i in range(4)):
#            plt.scatter(self.qt.p[self.bep[0]:self.bep[1], 0],
#                        self.qt.p[self.bep[0]:self.bep[1], 1],
#                        color='g', s=16, zorder=100)
            pass
        else:
            for c in self.c:
                if c:
                    c.plot()

    def find_leaf(self, x, y):
        for c in self.c:
            if c and c.sq.containing((x, y)):
                return c.find_leaf(x, y)
        # then now we are on a leaf or highest inner node containing (x, y)
        print(self.qt.p[self.bep[0]:self.bep[1]])
        print(self)
        if self.sq.L > 1 and self.bep[1] - self.bep[0] > self.qt.k:
            print('inner')
        else:
            print('leaf')
        print(self.__neighbors())

    def __neighbors(self):
        base = [self.qt.lt.neighbor(self.lc, i) for i in range(8)]
        B = [c if len(str(c)) <= self.h else None for c in base]
        print('0(E), 1(NE), 2(N), 3(NW), 4(W), 5(SW), 6(S), 7(SE)')
        return [str(c).zfill(self.h)
                if str(c).zfill(self.h) in self.qt.loc else None for c in B]


class quadtree:
    """
    Quadtree class (static)

    One of the main purpose of this class is in order to use
    in PTAS for the Euclidean TSP

    Parameters
    ----------
    points : numpy array (2d array)
        points in 2d Euclidean space. In our application, this is an instance
        of Euclidean traveling salseman problems

    k : int
        maximum strage capacity; each node of this quadtree is permitted
        having no more than k points.

    leaves: dict
        pointing from a stored point (of TSP instance) to the heighest
        level quadtree node containing it.

    loc: dict
        pointing from any location code to the corresponding quadtree node
        if exists. this is used for checking whether same level neighbors
        exist.
    """
    lt = None

    def __init__(self, points, k=1):
        self.p = points
        self.k = k
        self.leaves = {}
        self.loc = {}
        self.qt = node(self, (0, len(self.p)),
                       square(*self.__bounding_square()), 0, 0, None)

    def __bounding_square(self):
        L, _max = 1, self.p.max()
        while L < _max:
            L <<= 1
        return 0, 0, L

    def draw(self):
        """
        Draw current quadtree structures
        """
        plt.cla()
        self.qt.plot()

        plt.gca().set_aspect('equal')
        plt.autoscale()
        plt.tight_layout()

    def find_leaf(self, x, y):
        """
        Find the highest level node containing given point (x, y)

        Parameters
        ----------
            x : int
                x-coordinate
            y : int
                y-coordinate
        """
        if not self.qt.sq.containing((x, y)):
            return
        self.qt.find_leaf(x, y)


def gen(n, w, seed=0):
    np.random.seed(seed)
    return np.random.randint(0, w, (n, 2))


qt = None


def onclick(event):
    qt.find_leaf(event.xdata, event.ydata)
    print()


if __name__ == '__main__':
    qt = quadtree(gen(20, 1 << 10))
    qt.draw()
    plt.savefig('q1.png', bbox_inches='tight')
    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()
