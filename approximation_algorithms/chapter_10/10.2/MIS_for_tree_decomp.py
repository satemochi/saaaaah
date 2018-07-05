class max_independent_set_with_tree_decomposition:
    def __init__(self, g, t):
        self.g = g
        self.t = t
        self.checked = [v for v in t.nodes() if t.degree(v) == 1]
        self.__init_table()
        self.__init_waiting_queue()
        self.__solve()

    def __init_table(self):
        self.T = {v: self.__feasible_family(v) for v in self.checked}

    def __feasible_family(self, v):
        return [u for u in self.__powerset(v) if self.__independence(u)]

    def __powerset(self, s):
        n = len(s)
        for i in xrange(1 << n):
            yield set([s[j] for j in xrange(n) if (i & (1 << j))])

    def __independence(self, vertices):
        for v in vertices:
            if any(w in vertices for w in self.g[v]):
                return False
        return True

    def __init_waiting_queue(self):
        self.waiting = []
        for v in self.checked:
            self.__update_queue(v)

    def __update_queue(self, v):
        w = self.__find_next(v)
        if w is not None and w not in self.waiting:
            self.waiting.append(w)

    def __find_next(self, v):
        nbr = [w for w in self.t[v] if w not in self.checked]
        if len(nbr) == 1:
            if len([w for w in self.t[nbr[0]] if w not in self.checked]) <= 1:
                return nbr[0]

    def __solve(self):
        while self.waiting:
            v = self.waiting.pop(0)
            self.checked.append(v)
            self.__update_table(v)
            self.__update_queue(v)
        self.__is = self.__getmax(self.checked[-1])

    def __update_table(self, v):
        children = [w for w in self.t[v] if w in self.checked]
        self.T[v] = []
        for u in self.__feasible_family(v):
            sub = u
            for w in children:
                max_, maxi_ = 0, None
                core = set(v) & set(w)
                for x in self.T[w]:     # solutions of sub-problems
                    if self.__compatible(core, u, x):
                        if max_ < self.__e(x):
                            max_ = self.__e(x)
                            maxi_ = x
                if maxi_ and len(maxi_) > 0:
                    sub |= maxi_    # children are independent by excluding u.
            self.T[v].append(sub)
        for w in children:
            del self.T[w]

    def __e(self, vertices):
        return sum(self.g.node[v]['w'] for v in vertices)

    def __compatible(self, core, u, w):
        return (core & u) == (core & w)

    def __getmax(self, v):
        max_, maxi_ = 0, None
        for x in self.T[v]:
            if max_ < self.__e(x):
                max_ = self.__e(x)
                maxi_ = x
        return maxi_

    @property
    def independent_set(self):
        return self.__is
