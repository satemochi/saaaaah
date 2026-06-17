from itertools import combinations
from unittest import TestCase, main
from splay import s_vertex


class forest:
    def __init__(self, n):
        """ Construct a forest with 'n' nodes. """
        self.__vertices = [s_vertex(i) for i in range(n)]

    def __access(self, u):
        """ Access a vertex 'u'.
            This does two things. Firstly 'u' is splayed within it's aux-tree.
            Secondly, iteratively move 'u' to the top tree of aux-trees.
            This guarantees that 'u' to the root is a preferred path. """
        v = self.__vertices[u]
        v.splay()
        if v.right is not None:
            v.right.deltaW += v.deltaW
            v.right.path_parent = v
            v.right.parent = None
            v.right = None

        while v.path_parent is not None:
            w = v.path_parent
            w.splay()
            if w.right is not None:
                w.right.deltaW += w.deltaW
                w.right.path_parent = w
                w.right.parent = None

            w.right = v
            v.parent = w
            v.path_parent = None
            v.deltaW -= w.deltaW
            w.update_delta_min()

            v.splay()

    def get(self, u):
        """ Return the weight of a vertex. """
        self.__access(u)
        return self.__vertices[u].deltaW

    def set(self, u, value):
        """ Set a weight of a vertex. """
        self.__access(u)
        v = self.__vertices[u]
        if v.left is not None:
            v.left.deltaW += v.deltaW - value
        if v.right is not None:
            v.right.deltaW += v.deltaW - value
        v.deltaW = value
        v.update_delta_min()

    def link(self, src, sink, weight):
        """ Add a directed edge '(src, sink)' with a certain weight.
            This makes 'sink' the parent of 'src' in the rooted forest.
            Precondition: 'src' does not have a parent.  """
        self.__access(src)
        self.__access(sink)
        u, v = self.__vertices[src], self.__vertices[sink]

        assert u.left is None, "'u' already has a parent in represented tree."
        u.left = v
        assert v.parent is None, "'v' should not have parent after 'access'."
        v.parent = u

        v.deltaW -= u.deltaW
        u.update_delta_min()
        self.update_path(src, weight)
        self.update_path(sink, -weight)

    def cut(self, vertex):
        """ Cut the edge '(u, p(u))' where 'p(u)' is the parent of 'u'.
            Returns 'p(u)' or -1 if no parent exists.  """
        self.__access(vertex)
        u, v = self.__vertices[vertex], self.__vertices[vertex].left
        if v is None:
            return -1
        v.parent = None
        u.left = None
        v.deltaW += u.deltaW
        u.update_delta_min()
        v.update_delta_min()
        return v.id

    def connected(self, u, v):
        """ Return true if 'u' and 'v' are part of the same tree.
            This is done by calling 'findRoot' twice.  """
        return self.find_root(u) == self.find_root(v)

    def find_root(self, u):
        """ Find the root of 'u'.  """
        self.__access(u)
        v = self.__vertices[u]
        while v.left is not None:
            v = v.left
        self.__access(v.id)
        return v.id

    def find_parent(self, u):
        """ Return parent of vertex of -1 if no such parent exists.  """
        self.__access(u)
        v = self.__vertices[u]
        if v.left is not None:
            v = v.left
            while v.right is not None:
                v = v.right
            self.__access(v.id)
            return v.id
        return -1

    def find_root_edge(self, vertex):
        """ Find the edge in a path which points to the root.
            Example:
                With the following directed path 'find_root_edge(a)' should
                result in vertex 'd' since edges are represented by their tail.
                        a -> b -> c -> d -> root    """
        self.__access(vertex)
        u = self.__vertices[vertex]
        while u.left is not None and u.left.left is not None:
            u = u.left
        if u.left.right is not None:
            u = u.left.right
            while u.left is not None:
                u = u.left
        self.__access(u.id)
        return u.id

    def find_path_min(self, vertex):
        """ Find minimum value along path from 'u' to root.
            Return pair '(val, vertex)'.
            If several vertices have the same minimum value, the vertex
            closest to the root is returned.  """
        self.__access(vertex)
        u = self.__vertices[vertex]
        weight = u.deltaW
        if u.left is None:
            return weight, u.id

        """ minWeight := minimum of root of aux-tree and left branch of
            aux-tree. Don't consider right side of aux-tree as that is further
            down path in represented tree.  """
        minWeight = min(weight, weight + u.left.deltaW + u.left.deltaMin)
        minVertex = u if weight == minWeight else None
        u = u.left
        weight += u.deltaW

        if weight == minWeight:
            minVertex = u

        while u.left is not None or u.right is not None:
            if u.left is not None:
                lWeight = weight + u.left.deltaW
                lMin = lWeight + u.left.deltaMin
                if lWeight == minWeight:
                    minVertex = u.left
                if lMin == minWeight:
                    u = u.left
                    weight = lWeight
                    continue
            if u.right is not None and u != minVertex:
                rWeight = weight + u.right.deltaW
                rMin = rWeight + u.right.deltaMin
                if rWeight == minWeight:
                    minVertex = u.right
                if rMin == minWeight:
                    u = u.right
                    weight = rWeight
                    continue
            break
        return minWeight, minVertex.id

    def update_path(self, vertex, delta):
        """ Add integer 'delta' to all vertices on the path from 'vertex'
            to the root.  """
        self.__access(vertex)
        u = self.__vertices[vertex]
        u.deltaW += delta
        if u.right is not None:
            u.right.deltaW -= delta
        u.update_delta_min()

    def update_path_edges(self, u, delta):
        """ Add an integer 'delta' to all edges along a path from 'u'
            to the root.  """
        self.__access(vertex)
        u = self.__vertices[vertex]
        u.deltaW += delta
        while u.left is not None:
            u = u.left
        u.deltaW -= delta
        while u.parent is not None:
            u.parent.update_delta_min()
            u = u.parent

    def reset(self, begin, end):
        """ Iterate over subset of vertices and clear all parent and child
            pointers as well as setting weights to 0.
        """
        for v in self.__vertices[begin:end]:
            v.reset()

    def __repr__(self):
        """ Print available information to the output stream without modifying
            the datastructure.  """
        s = f"Link-cut forest of size {n}:\n"
        for i, v in enumerate(self.__vertices):
            s += f"{i}\n"
            if v.parent is not None:
                s += f"\tParent: {v.parent.id}\n"
            if v.left is not None:
                s += f"\tLeft: {v.left.id}\n"
            if v.right is not None:
                s += f"\tRight: {v.right.id}\n"
        return s


class test_linkcut_tree(TestCase):
    def test_construct_empty(self):
        f = forest(n := 10)
        for u, v in combinations(range(n), 2):
            self.assertFalse(f.connected(u, v))

    def test_link_single(self):
        f = forest(n := 10)
        f.link(0, 1, 50)
        self.assertTrue(f.connected(0, 1))
        self.assertEqual(f.find_root(0), 1)
        self.assertEqual(f.find_root(1), 1)

    def test_link_three(self):
        f = forest(n := 3)
        f.link(0, 2, 50)
        f.link(1, 2, 30)
        self.assertTrue(f.connected(0, 1))
        self.assertTrue(f.connected(0, 2))
        self.assertTrue(f.connected(1, 2))

    def test_link_path(self):
        f = forest(n := 10)
        for i in range(n-1):
            f.link(i, i+1, 50)
        for i in range(n-1):
            self.assertEqual(f.find_root(i), n-1)
        for u, v in combinations(range(n), 2):
            self.assertTrue(f.connected(u, v))

    def test_link_then_cut_single(self):
        f = forest(n := 2)
        f.link(0, 1, 50)
        self.assertTrue(f.connected(0, 1))
        f.cut(0)
        self.assertFalse(f.connected(0, 1))

    def test_link_then_cut_path(self):
        f = forest(n := 10)
        for i in range(n-1):
            f.link(i, i+1, 42)
        f.cut(n // 2)
        for i in range(n//2+1):
            for j in range(n//2+1, n):
                self.assertFalse(f.connected(i, j))

    def test_link_binary_tree(self):
        """ Construct a balanced binary tree. Check that all vertices share
            the same root. """
        f = forest(n := (1 << 5) - 1)
        for i in range(2, n+1):
            p = i // 2
            f.link(i - 1, p - 1, 42)
        for i in reversed(range(n-1)):
            self.assertEqual(f.find_root(i), 0)

    def test_link_then_cut_binary_tree(self):
        """ Construct a balanced binary tree, then remove edges in middle
            layer. """
        f = forest(n := (1 << 8) - 1)
        #  Use 1-indexing => children of node 'p' are '2p' and '2p+1'
        for u in range(2, n+1):
            p = u // 2
            f.link(u - 1, p - 1, 42)
        # Remove layers between layer 2 and 3.
        for u in range(1 << 3, 1 << 4):
            f.cut(u)
        self.assertTrue(f.connected((1 << 3) * 2, ((1 << 3) * 2 + 1) * 2))
        self.assertFalse(f.connected((1 << 3) * 2, (1 << 3) + 2))
        self.assertTrue(f.connected(1 << 2, (1 << 2) + 1))

    def test_find_path_min_of_disconnected_forest(self):
        """ Each vertex in a disconnected forest should have return itself with
            'find_path_min'. """
        f = forest(n := 10)
        for u in range(n):
            w, r = f.find_path_min(u)
            self.assertEqual(w, 0)
            self.assertEqual(r, u)
        for u in range(n):
            f.update_path(u, u)
        for u in range(n):
            w, r = f.find_path_min(u)
            self.assertEqual(w, u)
            self.assertEqual(r, u)

    def test_find_path_min_of_path(self):
        """ Create single path, increment out of order, query 'find_path_min'
        """
        p = forest(n := 10)
        for u in range(1, n):
            p.link(u, u-1, 0)
        p.update_path(0, 5)
        w, r = p.find_path_min(0)
        self.assertEqual(w, 5)
        self.assertEqual(r, 0)

        p.update_path(5, 3)
        w, r = p.find_path_min(5)
        self.assertEqual(w, 3)
        self.assertEqual(r, 1)

        w, r = p.find_path_min(7)
        self.assertEqual(w, 0)
        self.assertEqual(r, 6)

        w, r = p.find_path_min(6)
        self.assertEqual(w, 0)
        self.assertEqual(r, 6)

    def test_link_non_zero_weight(self):
        """ Call 'link' with non-zero weight and verify that the weight is
            placed on the 'from' vertex. """
        f = forest(n := 2)
        f.link(0, 1, 42)
        w, r = f.find_path_min(0)
        self.assertEqual(w, 0)
        self.assertEqual(r, 1)
        w, r = f.find_path_min(1)
        self.assertEqual(w, 0)
        self.assertEqual(r, 1)

    def test_link_twice_non_zero_weight(self):
        """ Construct balanced tree with three vertices, perform
            'find_path_min' queries. """
        f = forest(n := 3)
        f.update_path(0, 1000)
        f.link(1, 0, 42)
        f.link(2, 0, 314)

        w, r = f.find_path_min(0)
        self.assertEqual(w, 1000)
        self.assertEqual(r, 0)

        w, r = f.find_path_min(1)
        self.assertEqual(w, 42)
        self.assertEqual(r, 1)

        w, r = f.find_path_min(2)
        self.assertEqual(w, 314)
        self.assertEqual(r, 2)

    def test_find_path_min_of_link_path(self):
        """ Create single path using non-zero weight to 'link' call.
            Query 'find_path_min' """
        p = forest(n := 10)
        p.update_path(0, 1000)
        p.link(1, 0, 8)
        p.link(2, 1, 9)
        p.link(3, 2, 1)
        p.link(4, 3, 1)
        p.link(5, 4, 18)
        p.link(6, 5, -1)
        p.link(7, 6, 9)
        p.link(8, 7, 3)
        p.link(9, 8, 2)

        w, r = p.find_path_min(6)
        self.assertEqual(w, -1)
        self.assertEqual(r, 6)

        w, r = p.find_path_min(4)
        self.assertEqual(w, 1)
        self.assertEqual(r, 3)

        w, r = p.find_path_min(9)
        self.assertEqual(w, -1)
        self.assertEqual(r, 6)

        w, r = p.find_path_min(0)
        self.assertEqual(w, 1000)
        self.assertEqual(r, 0)

        w, r = p.find_path_min(5)
        self.assertEqual(w, 1)
        self.assertEqual(r, 3)

        w, r = p.find_path_min(3)
        self.assertEqual(w, 1)
        self.assertEqual(r, 3)


if __name__ == '__main__':
    main()
