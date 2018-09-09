from copy import deepcopy
from functools import total_ordering
from itertools import combinations, ifilterfalse
from random import random, sample
from matplotlib import pyplot as plt
import networkx as nx


@total_ordering
class individual:
    def __init__(self, g, elimination_order):
        self.g = g.copy()
        self.chromosome = elimination_order
        self.fitness = self._tree_width()

    def _tree_width(self):
        return max(self._partial_clique(u) for u in self.chromosome)

    def _partial_clique(self, u):
        c = len(list(self.g[u]))
        self._make_simplicial(u)
        self.g.remove_node(u)
        return c

    def _make_simplicial(self, u):
        for i, j in combinations(self.g[u], 2):
            if not self.g.has_edge(i, j):
                self.g.add_edge(i, j)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.fitness == other.fitness

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.fitness < other.fitness


class ga_tw:
    def __init__(self, g, max_generation=10, population_size=100,
                 max_tournament_entries=30, crossover_rate=0.9,
                 mutation_rate=0.01, ):
        self.g = g
        self.n = g.number_of_nodes()
        self.max_generation = max_generation
        self.population_size = population_size
        self.max_tournament_entries = max_tournament_entries
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.best_individual = None
        self.current_generation = []
        self.next_generation = []

        self.__run()
        print self.best_individual.fitness

    def __run(self):
        self.__init_population()
        for i in xrange(self.max_generation):
            self.__progress()
            self.__generation_shift()

    def __init_population(self):
        n, vertices = self.g.number_of_nodes(), list(self.g.nodes())
        for i in xrange(self.population_size):
            chromosome = sample(vertices, n)
            self.current_generation.append(individual(self.g, chromosome))
        self.best_individual = min(i for i in self.current_generation)

    def __progress(self):
        passed = []
        while len(self.next_generation) < self.population_size:
            mum = self.__tournament_selection().chromosome
            dad = self.__tournament_selection().chromosome
            alice, bob = self.__crossover(mum, dad)
            self.__mutation(alice)
            self.__mutation(bob)
            if alice not in passed:
                self.next_generation.append(individual(self.g, alice))
                passed.append(alice)
            if bob not in passed:
                self.next_generation.append(individual(self.g, bob))
                passed.append(bob)

    def __crossover(self, mum, dad):
        if random() > self.crossover_rate:
            alice, bob = deepcopy(mum), deepcopy(dad)
            return alice, bob
        crossover_type = random()
        if crossover_type < 1./3:
            return self.__order_crossover(mum, dad)
        if crossover_type < 2./3:
            return self.__order_based_crossover(mum, dad)
        return self.__position_based_crossover(mum, dad)

    def __order_crossover(self, mum, dad):
        alice, bob = [-1] * self.n, [-1] * self.n
        a, b = self.__random_interval()
        self.__icopy(mum, alice, xrange(a, b+1))
        self.__icopy(dad, bob, xrange(a, b+1))
        self.__circular_copy(dad, alice, b+1)
        self.__circular_copy(mum, bob, b+1)
        return alice, bob

    def __random_interval(self):
        a, b = sample(xrange(self.n), 2)
        return (a, b) if a < b else (b, a)

    def __icopy(self, parent, child, crange):
        for i in crange:
            child[i] = parent[i]

    def __circular_copy(self, parent, offspring, start_pos):
        for i, c in enumerate(ifilterfalse(lambda x: x in offspring, parent)):
            offspring[(start_pos + i) % self.n] = c

    def __order_based_crossover(self, mum, dad):
        alice, bob = deepcopy(dad), deepcopy(mum)
        pos = self.__coin_tossing()
        m, d = [mum[i] for i in pos], [dad[i] for i in pos]
        mi = [i for i in xrange(self.n) if mum[i] in d]
        di = [i for i in xrange(self.n) if dad[i] in m]
        for i, x in zip(di, m):
            alice[i] = x
        for i, x in zip(mi, d):
            bob[i] = x
        return alice, bob

    def __coin_tossing(self):
        return [i for i in xrange(self.n) if random() < 0.5]

    def __position_based_crossover(self, mum, dad):
        alice, bob = [-1] * self.n, [-1] * self.n
        pos = self.__coin_tossing()
        self.__icopy(mum, alice, pos)
        self.__icopy(dad, bob, pos)
        self.__position_copy(dad, alice)
        self.__position_copy(mum, bob)
        return alice, bob

    def __position_copy(self, parent, offspring):
        blank_indices = [i for i in xrange(self.n) if offspring[i] == -1]
        to_be_fixed = ifilterfalse(lambda x: x in offspring, parent)
        for i, c in zip(blank_indices, to_be_fixed):
            offspring[i] = c

    def __mutation(self, chromosome):
        if random() > self.mutation_rate:
            return
        if random() < 1./2:
            self.__exchange_mutation(chromosome)
        else:
            self.__insertion_mutation(chromosome)

    def __exchange_mutation(self, chromosome):
        a, b = sample(xrange(self.n), 2)
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]

    def __insertion_mutation(self, chromosome):
        a, b = sample(xrange(self.n), 2)
        chromosome.insert(b, chromosome.pop(a))

    def __tournament_selection(self):
        return min(sample(self.current_generation, self.max_tournament_entries))

    def __generation_shift(self):
        del self.current_generation[:]
        self.current_generation, self.next_generation = self.next_generation, []

        _min = min(self.current_generation)
        if self.best_individual > _min:
            self.best_individual = _min


def gen(n=100):
    while True:
        g = nx.random_geometric_graph(n, 15./n)
        if nx.number_connected_components(g) == 1:
            return g


if __name__ == '__main__':
    x = ga_tw(gen())
