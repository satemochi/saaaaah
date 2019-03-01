from collections import deque


class conflict_pair:
    __slots__ = ('c')

    def __init__(self, h):
        self.c = [deque([h]), deque()]

    def __repr__(self):
        return ('\33[1m\33[90m(\33[0m' + str(list(self.c[0])) +
                ', ' + str(list(self.c[1])) + '\33[1m\33[90m)\33[0m')

    @property
    def l_empty(self):
        return len(self.c[0]) == 0

    @property
    def r_empty(self):
        return len(self.c[1]) == 0

    @property
    def left(self):
        return self.c[0]

    @property
    def right(self):
        return self.c[1]

    @property
    def l_lo(self):
        return self.c[0][-1]

    @property
    def l_hi(self):
        return self.c[0][0]

    @property
    def r_lo(self):
        return self.c[1][-1]

    @property
    def r_hi(self):
        return self.c[1][0]


class constraint_list:
    __slots__ = ('cp_list')

    def __init__(self, h=None):
        self.cp_list = deque([conflict_pair(h)]) if h is not None else deque()

    def __len__(self):
        return len(self.cp_list)

    def __lt__(self, other):
        if not isinstance(other, constraint_list):
            return NotImplemented
        diff = self.L.l_lo - other.L.l_lo
        if diff != 0:
            return diff < 0
        else:
            return self.H.l_hi < other.H.l_hi

    def __eq__(self, other):
        if not isinstance(other, constraint_list):
            return NotImplemented
        return self.L.l_lo == other.L.l_lo

    def __repr__(self):
        return ('\33[1m\33[91m{\33[0m' +
                ' '.join([repr(c) for c in self.cp_list]) +
                '\33[91m\33[1m}\33[0m')

    @property
    def empty(self):
        return len(self) == 0

    @property
    def H(self):
        return self.cp_list[0]

    @property
    def L(self):
        return self.cp_list[-1]

    def _oneSided(self):
        if not self.H.r_empty:
            return False
        for i in xrange(1, len(self.cp_list)):
            if not self.cp_list[i].r_empty:
                return False
            self.H.left.extend(self.cp_list[i].left)
        self.cp_list = deque([self.cp_list[0]])
        return True

    def merge(self, other):
        # assert(not self.empty and not other.empty)
        # assert(self < other or self == other)

        if not other._oneSided():
            return False

        while (self.H.r_empty and self.H.l_hi > other.H.l_lo):
            other.H.right.extend(self.H.left)
            self.cp_list.popleft()

        if self.H.r_empty:
            if self.L.l_hi == other.H.l_lo:
                other.H.left.pop()
                if (other.H.l_empty or (not other.H.r_empty and
                                        other.H.l_lo > other.H.r_lo)):
                    other.H.left, other.H.right = other.H.right, other.H.left
        else:
            hi = 1 if self.H.l_hi < self.H.r_hi else 0
            lo = -hi + 1
            if other.H.l_lo < self.H.c[lo][0]:
                return False
            elif other.H.l_lo < self.H.c[hi][0]:
                self.H.c[lo].extendleft(other.H.left)
                self.H.c[hi].extendleft(other.H.right)
                other.H.left.clear()
                other.H.right.clear()

        if not other.H.l_empty:
            self.cp_list.extendleft([other.H])

        return True

    def prune(self, dfs_height):
        while (not self.empty and not self.H.l_empty and
               self.H.l_hi >= dfs_height-1):
            if len(self.H.left) == 1:
                self.cp_list.popleft()
            else:
                self.H.left.popleft()
        while (not self.empty and not self.H.r_empty and
               self.H.r_hi >= dfs_height-1):
            self.H.right.popleft()
