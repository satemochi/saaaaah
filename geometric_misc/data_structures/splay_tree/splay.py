from unittest import TestCase, main


class s_vertex:
    def __init__(self, _id, left=None, right=None, parent=None,
                 path_parent=None, deltaW=0, deltaMin=0):
        self.id = _id
        self.left, self.right = left, right
        self.parent = parent
        self.path_parent = path_parent
        self.deltaW = deltaW
        self.deltaMin = deltaMin

    def __eq__(self, other):
        return self is not None and other is not None and self.id == other.id

    def __repr__(self):
        return str(self.id)

    def rotate_up(self):
        rf""" Rotate current vertex upwards. Let 'u' be the current vertex,
            'p' the parent, and A, B, C be subtrees. Then a rotation of 'u' is
            one of the following:
                    p           u        |       p            u
                   / \         / \       |      / \          / \
                  u   C  =>   A   p      |     A   u   =>   p   C
                 / \             / \     |        / \      / \
                A   B           B   C    |       B   C    A   B

            Maintains 'deltaW' and 'deltaMin'
        """
        u, p = self, self.parent
        if p is None:
            return
        u.path_parent = p.path_parent
        p.path_parent = None
        uDeltaW, pDeltaW = u.deltaW, p.deltaW
        u.deltaW = uDeltaW + pDeltaW
        p.deltaW = -uDeltaW

        if p.left == u:
            p.left = u.right
            if p.left is not None:
                p.left.parent = p
                p.left.deltaW += uDeltaW
            u.right = p
            u.parent = p.parent
            p.parent = u
        else:
            p.right = u.left
            if p.right is not None:
                p.right.parent = p
                p.right.deltaW += uDeltaW
            u.left = p
            u.parent = p.parent
            p.parent = u
        if u.parent is not None:
            if u.parent.left == p:
                u.parent.left = u
            elif u.parent.right == p:
                u.parent.right = u
        # Notice the order, 'p' is below 'u' in tree and must be updated first.
        p.update_delta_min()
        u.update_delta_min()

    def splay(self):
        """ Splay this vertex. """
        while self.parent is not None:
            if self.parent.parent is None:
                self.rotate_up()
            else:
                zigzigCase = (
                        (self.parent.left == self and
                         self.parent.parent.left == self.parent) or
                        (self.parent.right == self and
                         self.parent.parent.right == self.parent))
                if zigzigCase:
                    self.parent.rotate_up()
                    self.rotate_up()
                else:
                    self.rotate_up()
                    self.rotate_up()

    def update_delta_min(self):
        """ Update the 'deltaMin' property of the current vertex assuming its
            children maintain the 'deltaMin' invariant.
            'u.minWeight = u.weight + u.deltaMin'
        """
        left, right = 1 << 30, 1 << 30
        if self.left is not None:
            left = self.left.deltaW + self.left.deltaMin
        if self.right is not None:
            right = self.right.deltaW + self.right.deltaMin
        self.deltaMin = min(0, left, right)

    def reset(self):
        """ Clear all pointers and set weights to 0. This might result
            in neighboring vertices having broken invariants.
        """
        self.left, self.right, self.parent = None, None, None
        self.path_parent, self.deltaW, self.deltaMin = None, 0, 0


class test_splay_trees(TestCase):
    def test_single_rotation_with_singleton(self):
        u = s_vertex(0)
        u.rotate_up()
        self.assertEqual(u.parent, None)
        self.assertEqual(u.left, None)
        self.assertEqual(u.right, None)

    def test_single_rotation_with_left_child(self):
        u, p = s_vertex(0), s_vertex(1)
        u.parent, p.left = p, u
        u.rotate_up()

        self.assertEqual(u.parent, None)
        self.assertEqual(u.left, None)
        self.assertEqual(u.right, p)

        self.assertEqual(p.parent, u)
        self.assertEqual(p.left, None)
        self.assertEqual(p.right, None)

    def test_single_rotation_with_right_child(self):
        u, p = s_vertex(0), s_vertex(1)
        u.parent, p.right = p, u
        u.rotate_up()

        self.assertEqual(u.parent, None)
        self.assertEqual(u.left, p)
        self.assertEqual(u.right, None)

        self.assertEqual(p.parent, u)
        self.assertEqual(p.left, None)
        self.assertEqual(p.right, None)

    def test_full_left_rotation_with_both_children(self):
        rf"""
                    p           u
                   / \         / \
                  u   C  =>   A   p
                 / \             / \
                A   B           B   C
        """
        u, p = s_vertex(0), s_vertex(1)
        a, b, c = s_vertex(2), s_vertex(3), s_vertex(4)

        u.parent, p.left = p, u
        a.parent, u.left = u, a
        b.parent, u.right = u, b
        c.parent, p.right = p, c
        u.rotate_up()

        self.assertEqual(u.parent, None)
        self.assertEqual(u.left, a)
        self.assertEqual(u.right, p)

        self.assertEqual(p.parent, u)
        self.assertEqual(p.left, b)
        self.assertEqual(p.right, c)

        self.assertEqual(a.parent, u)
        self.assertEqual(b.parent, p)
        self.assertEqual(c.parent, p)

    def test_full_right_rotation_with_both_children(self):
        rf"""
                    p            u
                   / \          / \
                  A   u   =>   p   C
                     / \      / \
                    B   C    A   B
        """
        u, p = s_vertex(0), s_vertex(1)
        a, b, c = s_vertex(2), s_vertex(3), s_vertex(4)

        u.parent, p.right = p, u
        a.parent, p.left = p, a
        b.parent, u.left = u, b
        c.parent, u.right = u, c
        u.rotate_up()

        self.assertEqual(u.parent, None)
        self.assertEqual(u.left, p)
        self.assertEqual(u.right, c)

        self.assertEqual(p.parent, u)
        self.assertEqual(p.left, a)
        self.assertEqual(p.right, b)

        self.assertEqual(a.parent, p)
        self.assertEqual(b.parent, p)
        self.assertEqual(c.parent, u)


if __name__ == '__main__':
    main()
