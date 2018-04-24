

class location_pointer:
    """
    Resolving location codes in quadtrees.

    We based on Gargantini's binary representations for quad trees and
    Schrack's procedures for finding neighbors at same level.

    REFERENCES:
     - G. Schrack (1992), "Finding Neighbors of Equal Size in Linear
       Quadtrees and Octrees in Constant Time," CVGIP, pp.221-230.
     - I. Gargantini (1982), "An Effective Way to Represent Quadtrees,"
       Comm. ACM, vol. 25, pp. 905-910.
    """
    
    (E, NE, N, NW, W, SW, S, SE) = range(8)

    def __init__(self, level=10):
        self.maxlevel = level
        self.delta = [1, 3, 2, 0, 0, 0, 0, 0]
        self._x, self._y = 0, 0
        self.__preprocessing()

    def __preprocessing(self):
        for i in xrange(self.maxlevel):
            self._x = (self._x << 2) + 1
            self._y = (self._y << 2) + 2
        self.delta[self.W] = self._x
        self.delta[self.S] = self._y
        self.delta[self.NW] = self.delta[self.N] + self.delta[self.W]
        self.delta[self.SW] = self.delta[self.S] + self.delta[self.W]
        self.delta[self.SE] = self.delta[self.S] + self.delta[self.E]

    def parent(self, loc):
        """
        Get parent location code for given one

        Parameters
        ----------
        loc : int
            The target location code
        """
        return int(loc / 10)

    def children(self, loc):
        """
        Get list of children location codes for given one

        Parameters
        ----------
        loc : int
            The target location code
        """
        base = loc * 10
        return [base, base + 1, base + 2, base + 3]

    def neighbor(self, loc, i):
        """
        Get the neighbor location code for given one,
        with respect to a specified direction

        Parameters
        ----------
        loc : int
            The target location code
        i : int
            A direction of one of the adjacent 8-neighbors
            i.e.) 0(E), 1(NE), 2(N), 3(NW), 4(W), 5(SW), 6(S), 7(SE)
        """
        assert(self.E <= i and i <= self.SE)
        m = self.__neighbor(self.__to_binary(loc), i)
        return self.__to_location(m)

    def __neighbor(self, b, i):
        x = ((b | self._y) + (self.delta[i] & self._x)) & self._x
        y = ((b | self._x) + (self.delta[i] & self._y)) & self._y
        return x | y

    def __to_binary(self, loc):
        x, y, i = 0, 0, 0
        while loc > 0:
            digit = loc % 10
            if digit & 1: x += 1 << i
            if digit > 1: y += 1 << i
            loc, i = (loc - digit) / 10, i + 1
        return self.__slitting(x) | (self.__slitting(y) << 1)

    def __slitting(self, b):
        s, i = 0, 0
        while b:
            s, i, b = s + ((b & 1) << i), i + 2, b >> 1
        return s

    def __to_location(self, b):
        x, y = self.__concatting(b), self.__concatting(b >> 1)
        loc, a = 0, 1
        while x or y:
            xd, yd = x & 1, y & 1
            if xd == 0 and yd == 0: loc += 0 * a
            elif xd == 1 and yd == 0: loc += 1 * a
            elif xd == 0 and yd == 1: loc += 2 * a
            else: loc += 3 * a
            a, x, y = a * 10, x >> 1, y >> 1
        return loc

    def __concatting(self, b):
        c, i = 0, 0
        while b:
            c, i, b = c + ((b & 1) << i), i + 1, b >> 2
        return c


if __name__ == '__main__':
    n = 200
    print n
    locp = location_pointer()
    print locp.neighbor(n, 2)
    print locp.parent(n)
    print locp.children(n)
    help(location_pointer)
