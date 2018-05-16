from bisect import bisect_left, insort
from collections import defaultdict

from intersect import intersect
from sweep_line import sweep_line


class line_intersections:
    """
    Bentley-Ottman algorithm
    """
    sentinels = [float('-inf'), float('inf')]

    def __init__(self, segs):
        self.segs = segs
        self.sl = sweep_line(segs)
        self.events = []
        for i, (p, q) in enumerate(segs):
            self.events.append((p, i, p[0] <= q[0]))
            self.events.append((q, i, q[0] < p[0]))
        self.events.sort()
        # We need this hash, to avoid repeatedly reporting same intersections.
        self.reported = defaultdict(lambda: False)

    def __test_intersect(self, i, j):
        if i in self.sentinels or j in self.sentinels:
            return
        pair = (i, j) if i < j else (j, i)  # i, j may tip over on processing.
        if self.reported[pair]:
            return
        x, y = intersect(self.segs[i], self.segs[j])
        if x:
            insort(self.events, ((x, y), (i, j), None))  # swap-event
            self.reported[pair] = True
            return (x, y)

    def left_event(self, p, i):
        b, a = self.sl.neighbors(p)
        self.sl.insert(p, i)
        c, d = self.__test_intersect(b, i), self.__test_intersect(i, a)
        if c:
            yield c
        if d:
            yield d

    def right_event(self, p, i):
        self.sl.delete(p, i)
        b, a = self.sl.neighbors(p)
        return self.__test_intersect(b, a)

    def swap_event(self, p, (i, j)):
        bp, ap = self.sl.swap(p, i, j)
        if bp is not None:
            bc, ac = self.__test_intersect(*bp), self.__test_intersect(*ap)
            if bc:
                yield bc
            if ac:
                yield ac

    def search(self):
        while self.events:
            end_point, index, event_type = self.events.pop(0)
            if event_type is None:
                for c in self.swap_event(end_point, index):
                    yield c
            elif event_type:
                for c in self.left_event(end_point, index):
                    yield c
            else:
                c = self.right_event(end_point, index)
                if c:
                    yield c
