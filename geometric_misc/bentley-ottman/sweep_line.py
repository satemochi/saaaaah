class sweep_line:
    def __init__(self, segments):
        self.ilist = [float('-inf'), float('inf')]
        self.segs = segments

    def insert(self, p, i):
        self.ilist.insert(self.__pos(p), i)

    def delete(self, p, i):
        k = self.__pos(p)
        if self.ilist[k] == float('-inf'):
            k = 1
        if self.ilist[k] == float('inf'):
            k -= 1
        "TODO: you should be able to describe more simply."
        if i != self.ilist[k]:
            k -= 1
        assert(self.ilist[k] == i)
        self.ilist.pop(k)

    def swap(self, p, i, j):
        assert(len(self.ilist) > 3)
        k = self.__pos(p)
        "TODO: you should be able to describe more simply."
        for pos, idx in enumerate(self.ilist[k-1:k+2], k-1):
            if idx == j:
                break
        assert(pos != 0)
        assert(i == self.ilist[pos-1] and j == self.ilist[pos])
        self.ilist[pos-1], self.ilist[pos] = self.ilist[pos], self.ilist[pos-1]
        return ((self.ilist[pos-2], self.ilist[pos-1]),
                (self.ilist[pos], self.ilist[pos+1]))

    def neighbors(self, p):
        i = self.__pos(p)
        return self.ilist[i-1], self.ilist[i]

    def __pos(self, (x, y)):
        left, right, pos = 0, len(self.ilist) - 1, 0
        while left < right:
            pos = (left + right) // 2
            y1, y2 = self.__get_interval(pos, x)

            if y1 <= y and y <= y2:
                "TODO: we have to describe more strictly;"
                " This condition may lead inconsistencies due to calc errors."
                " specifically, in equality tests when y1 > y2."
                " !!! This is the root of all evil !!!"
                break
            if y > y2:
                left = pos + 1
            elif y < y1:
                right = pos
        return pos + 1

    def __yintercept(self, s, x):
        assert(min(s[0][0], s[1][0]) <= x and x <= max(s[0][0], s[1][0]))
        dx, dy = s[1][0] - s[0][0], s[1][1] - s[0][1]
        return s[0][1] + (float(dy) / dx) * (x - s[0][0])

    def __get_interval(self, pos, x):
        y1, y2 = float('-inf'), float('inf')
        if self.ilist[pos] != y1:
            y1 = self.__yintercept(self.segs[self.ilist[pos]], x)
        if self.ilist[pos+1] != y2:
            y2 = self.__yintercept(self.segs[self.ilist[pos+1]], x)
        return y1, y2
