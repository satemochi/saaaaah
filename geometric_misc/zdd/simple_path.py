import networkx as nx


class simple_path:
    """ A frontier approach for enumerating simple paths with
        respect to Zero-suppressed decision diagrams (ZDD).
    """
    def __init__(self, graph, source, target, ordered=None):
        self.g = graph
        self.s, self.t = source, target
        self.universe = ordered if ordered else list(self.__bfs())
        self.status = [[{}], []]    # using at classification method
        self.__settle_ttl()         # Time to Live for maintaing expiration

    def __bfs(self):
        checked = []
        stack = [(self.s, iter(self.g[self.s]))]
        while stack:
            v, nbrs = stack[0]
            try:
                w = next(nbrs)
                if (v, w) in checked or (w, v) in checked:
                    continue
                checked.append((v, w))
                stack.append((w, iter(self.g[w])))
                yield v, w
            except StopIteration:
                stack.pop(0)

    def __settle_ttl(self):
        """ Given ordered universe, we can resolve expired timing
            for each vertices.
        """
        self.ttl = {}
        for v in self.g.nodes():
            indices = [self.universe.index((v, w))
                       for w in self.g[v] if (v, w) in self.universe]
            self.ttl[v] = max(indices) if len(indices) else 0

    def classification(self, dd, time, new_element):
        self.time, (self.u, self.v) = time, new_element
        self.frontier = {}
        for self.state in self.status[self.time % 2]:
            self.key = self.__get_key(self.state)
            self.zv = (time, self.key)
            self.__zero_edge(dd)
            self.__one_edge(dd)
            dd.node[self.zv]['label'] = time
        del self.status[self.time % 2][:]

    def __get_key(self, state):
        return hash(tuple((k, v) for k, v in state.items()))

    def __zero_edge(self, dd):
        e, state = None, dict(self.state)
        if (self.__illegal_expiration(self.u) or
                self.__illegal_expiration(self.v)):
            e = (self.zv, 'zero')
        else:
            self.__remove_expired(state)
            new_key = self.__get_key(state)
            e = (self.zv, (self.time+1, new_key))
            self.frontier[new_key] = (self.time+1, new_key)
            self.status[(self.time+1) % 2].append(state)
        dd.add_edge(*e, sign=0)

    def __illegal_expiration(self, v, state=None):
        if state is None:
            state = self.state
        if self.ttl[v] == self.time:
            if v in (self.s, self.t):
                if self.__degree(v, state) == 0:
                    return True
            else:
                if self.__degree(v, state) == 1:
                    return True
        return False

    def __degree(self, v, state=None):
        if state is None:
            state = self.state
        return 0 if v not in state or state[v] == v else \
               1 if state[v] != 0 else \
               2

    def __remove_expired(self, state):
        if self.u in state and self.ttl[self.u] == self.time:
            del state[self.u]
        if self.v in state and self.ttl[self.v] == self.time:
            del state[self.v]

    def __one_edge(self, dd):
        mtype = self.__is_feasible()
        if mtype is True:
            e = (self.zv, 'one')
        elif mtype is False:
            e = (self.zv, 'zero')
        else:
            state = dict(self.state)
            self.__update_state(state)
            if (self.__illegal_expiration(self.u, state) or
                    self.__illegal_expiration(self.v, state)):
                e = (self.zv, 'zero')
            else:
                self.__remove_expired(state)
                new_key = self.__get_key(state)
                if new_key in self.frontier:
                    e = (self.zv, self.frontier[new_key])
                else:
                    e = (self.zv, (self.time+1, new_key))
                    self.frontier[new_key] = (self.time+1, new_key)
                    self.status[(self.time+1) % 2].append(state)
        dd.add_edge(*e, sign=1)

    def __is_feasible(self):
        u, v = self.u, self.v
        self.mate_u = u if u not in self.state else self.state[u]
        self.mate_v = v if v not in self.state else self.state[v]
        if (self.__fork() or self.__illegal_terminal() or self.__cyclic()):
            return False
        return self.__is_legal_path()

    def __fork(self):
        return self.__degree(self.u) == 2 or self.__degree(self.v) == 2

    def __illegal_terminal(self):
        terms = (self.s, self.t)
        return ((self.u in terms and self.__degree(self.u) != 0) or
                (self.v in terms and self.__degree(self.v) != 0))

    def __cyclic(self):
        return self.u == self.mate_v or self.v == self.mate_u

    def __is_legal_path(self):
        if ((self.mate_u == self.s and self.mate_v == self.t) or
                (self.mate_v == self.s and self.mate_u == self.t)):
            for x in self.state:
                if self.__degree(x) != 2:
                    if x not in (self.s, self.t, self.u, self.v):
                        return False
            return True
        return None

    def __update_state(self, state):
        self.__entry(state)
        self.__refine_topologically(state)

    def __entry(self, state):
        state[self.u] = self.u if self.u not in state else state[self.u]
        state[self.v] = self.v if self.v not in state else state[self.v]

    def __refine_topologically(self, state):
        mu, mv = state[self.u], state[self.v]
        if self.__degree(self.u) == 1:
            state[self.u], state[mu] = 0, mv
        else:
            state[self.u] = mv
        if self.__degree(self.v) == 1:
            state[self.v], state[mv] = 0, mu
        else:
            state[self.v] = mu

    def get_root(self):
        return (0, self.__get_key({}))
