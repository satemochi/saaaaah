from abc import ABCMeta, abstractmethod
from copy import copy
from functools import reduce
import networkx as nx


__all__ = ['is_isomorphic',
           'vf2_iso', 'vf2_sub', 'vf2_mono',
           'vf2_iso_simple', 'vf2_sub_simple', 'vf2_mono_simple',
           'extra_homo']


def is_isomorphic(g1, g2, problem="graph"):
    if problem in 'GI graph isomorphisms':
        verifier = vf2_iso(g1, g2)
    elif problem in 'S (induced) subgraph isomorphisms':
        verifier = vf2_sub(g1, g2)
    elif problem in 'M monomorphisms graph matching':
        verifier = vf2_mono(g1, g2)
    elif problem in 'H homomorphisms':
        verifier = extra_homo(g1, g2)
    else:
        return

    if verifier.has_valid_global_properties():
        try:
            x = next(verifier.iterate_isomorphisms())
            return True
        except StopIteration:
            pass
    return False


class matcher(metaclass=ABCMeta):
    __slots__ = ('g1', 'g2', '_f1', '_f2', '_m1', '_m2')

    def __init__(self, g1, g2):
        self.g1, self.g2 = g1, g2
        self._f1, self._f2, self._m1, self._m2 = {}, {}, {}, {}

    @abstractmethod
    def has_valid_global_properties(self):
        """ describe (light-weight) necessary conditions """
        raise NotImplementedError()

    @property
    def mapping(self):
        """ (access point) an isomorphism from g1 to g2 """
        return self._f1

    @property
    def inverse(self):
        """ (access point) inverse of f1, i.e. a map from g2 to g1 """
        return self._f2

    def iterate_isomorphisms(self):
        """ enumerate all isomorphisms """
        stack = [self._generate_candidates()]
        while stack:
            try:
                v1, v2 = next(stack[-1])
                if self._is_feasible(v1, v2):
                    self._f1[v1], self._f2[v2] = v2, v1
                    if self._is_established():
                        yield self._f1
                        self._f1.popitem(), self._f2.popitem()
                    else:
                        self.__update_state(v1, v2)
                        stack.append(self._generate_candidates())
            except StopIteration:
                self.__restore_state()
                stack.pop()

    @abstractmethod
    def _generate_candidates(self):
        """ describe a generator producing pairs of nodes """
        raise NotImplementedError()

    @abstractmethod
    def _is_feasible(self):
        """ describe safe-matching / cutting rules """
        raise NotImplementedError()

    @abstractmethod
    def _is_established(self):
        """ describe yielding conditions for each problem types """
        raise NotImplementedError()

    def __update_state(self, v1, v2):
        self.__updates(self.g1, v1, self._f1, self._m1)
        self.__updates(self.g2, v2, self._f2, self._m2)

    @staticmethod
    def __updates(g, v, f, m):
        m[v] = len(f) if v not in m else m[v]
        m.update({w: len(f) + 1 for w in g[v] if w not in m})

    def __restore_state(self):
        self.__restores(self._f1, self._m1)
        self.__restores(self._f2, self._m2)

    @staticmethod
    def __restores(f, m):
        while m:
            v, d = m.popitem()
            if d < len(f):
                m[v] = d
                break
        if f:
            f.popitem()


class vf2_iso_simple(matcher):
    def has_valid_global_properties(self):
        return (self.g1.order() == self.g2.order() and
                self.g1.size() == self.g2.size() and
                sorted(d for _, d in self.g1.degree) ==
                sorted(d for _, d in self.g2.degree))

    def _generate_candidates(self):
        g1, g2 = self.g1, self.g2
        f1, f2, m1, m2 = self._f1, self._f2, self._m1, self._m2
        t1, t2 = [v for v in m1 if v not in f1], [v for v in m2 if v not in f2]
        (t, v2) = (t1, next(iter(t2))) if t1 and t2 else \
                  ([v for v in g1 if v not in f1], next(iter(set(g2)-set(f2))))
        for v1 in t:
            yield (v1, v2)

    def _is_feasible(self, v1, v2):
        n1, n2 = self.g1[v1], self.g2[v2]
        if (self._is_invalid_neighbor_constraint(n1, n2) or     # inner
                self._is_invalid_look_ahead_1(n1, n2) or        # middle
                self._is_invalid_look_ahead_2(n1, n2)):         # outer
            return False
        return True

    def _is_invalid_neighbor_constraint(self, n1, n2):
        return (any(u1 in self._f1 and self._f1[u1] not in n2 for u1 in n1) or
                any(u2 in self._f2 and self._f2[u2] not in n1 for u2 in n2))

    def _is_invalid_look_ahead_1(self, n1, n2):
        return (sum(1 for u in n1 if u in self._m1 and u not in self._f1) !=
                sum(1 for u in n2 if u in self._m2 and u not in self._f2))

    def _is_invalid_look_ahead_2(self, n1, n2):
        return (sum(1 for u in n1 if u not in self._m1) !=
                sum(1 for u in n2 if u not in self._m2))

    def _is_established(self):
        return len(self._f1) == self.g2.order()


class vf2_sub_simple(vf2_iso_simple):
    def has_valid_global_properties(self):
        return (self.g1.order() >= self.g2.order() and
                self.g1.size() >= self.g2.size())

    def _is_invalid_look_ahead_1(self, n1, n2):
        return (sum(1 for u in n1 if u in self._m1 and u not in self._f1) <
                sum(1 for u in n2 if u in self._m2 and u not in self._f2))

    def _is_invalid_look_ahead_2(self, n1, n2):
        return (sum(1 for u in n1 if u not in self._m1) <
                sum(1 for u in n2 if u not in self._m2))


class vf2_mono_simple(vf2_sub_simple):
    def _is_invalid_neighbor_constraint(self, n1, n2):
        return any(u2 in self._f2 and self._f2[u2] not in n1 for u2 in n2)


class vf2_iso(vf2_iso_simple):
    def _is_feasible(self, v1, v2):
        n1, n2 = self.g1[v1], self.g2[v2]
        if (self._is_invalid_self_loop_counts(v1, v2) or
                self._is_invalid_multiedge_counts(v1, n1, v2, n2) or
                self._is_invalid_neighbor_constraint(n1, n2) or     # inner
                self._is_invalid_look_ahead_1(n1, n2) or            # middle
                self._is_invalid_look_ahead_2(n1, n2)):             # outer
            return False
        return True

    def _is_invalid_self_loop_counts(self, v1, v2):
        return self._ec(self.g1, v1, v1) != self._ec(self.g2, v2, v2)

    def _is_invalid_multiedge_counts(self, v1, n1, v2, n2):
        g, h, f1, f2, e = self.g1, self.g2, self._f1, self._f2, self._ec
        return (any(u in f1 and e(g, v1, u) != e(h, v2, f1[u]) for u in n1) or
                any(w in f2 and e(g, f2[w], v1) != e(h, v2, w) for w in n2))

    def _ec(self, g, u, v):
        return g.number_of_edges(u, v)


class vf2_sub(vf2_iso):
    def has_valid_global_properties(self):
        return (self.g1.order() >= self.g2.order() and
                self.g1.size() >= self.g2.size())

    def _is_invalid_look_ahead_1(self, n1, n2):
        return (sum(1 for u in n1 if u in self._m1 and u not in self._f1) <
                sum(1 for u in n2 if u in self._m2 and u not in self._f2))

    def _is_invalid_look_ahead_2(self, n1, n2):
        return (sum(1 for u in n1 if u not in self._m1) <
                sum(1 for u in n2 if u not in self._m2))


class vf2_mono(vf2_sub):
    def _is_invalid_self_loop_counts(self, v1, v2):
        return self._ec(self.g1, v1, v1) < self._ec(self.g2, v2, v2)

    def _is_invalid_multiedge_counts(self, v1, n1, v2, n2):
        g, h, f1, f2, e = self.g1, self.g2, self._f1, self._f2, self._ec
        return (any(u in f1 and e(g, v1, u) < e(h, v2, f1[u]) for u in n1) or
                any(w in f2 and e(g, f2[w], v1) < e(h, v2, w) for w in n2))

    def _is_invalid_neighbor_constraint(self, n1, n2):
        return any(u2 in self._f2 and self._f2[u2] not in n1 for u2 in n2)


class extra_homo(matcher):
    def has_valid_global_properties(self):
        return (self.g1.order() >= self.g2.order() and
                self.g1.size() >= self.g2.size())

    def _generate_candidates(self):
        f1, g1, g2 = self._f1, self.g1, self.g2
        t1 = [v for v in self._m1 if v not in f1]
        v1 = next(iter(t1)) if t1 else next(iter(set(g1) - set(f1)))
        fv = [f1[u] for u in g1[v1] if u in f1]
        n2 = reduce(set.union, [set(g2[u]) for u in fv]) if fv else g2
        for v2 in n2:
            yield (v1, v2)

    def _is_feasible(self, v1, v2):
        n1, n2 = self.g1[v1], self.g2[v2]
        if any(u1 in self._f1 and self._f1[u1] not in n2 for u1 in n1):
            return False
        return True

    def _is_established(self):
        return len(self._f1) == self.g1.order()


def draw(g1, g2, f):
    if f is not None:
        print(f)
        pos1 = nx.spring_layout(g1)
        pos2 = {v: pos1[f[v]] for v in g2}

        from matplotlib import pyplot as plt
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
        nx.draw_networkx(g1, pos1, ax=ax1, node_color='orange')
        nx.draw_networkx(g1, pos1, ax=ax2, alpha=0.1)
        nx.draw_networkx(g2, pos2, ax=ax2, node_color='#ffcccc')

        ax1.set_aspect('equal')
        ax2.set_aspect('equal')
        ax1.axis('off')
        ax2.axis('off')
        # plt.savefig('frucht_vf2_ex2.png', bbox_inches='tight')
        plt.tight_layout()
        plt.show()
    else:
        print('non-isomorphic.')


def gen():
    g1 = nx.frucht_graph()
    g2 = nx.LCF_graph(12, [-5, -2, -4, 2, 5, -2, 2, 5, -2, -5, 4, 2], 1)
    return g1, g2


if __name__ == '__main__':
    g1, g2 = gen()

    if is_isomorphic(g1, g2):
        print('isomorphic')
        verifier = vf2_iso(g1, g2)
        f = next(verifier.iterate_isomorphisms())
        draw(g1, g2, verifier.inverse)
