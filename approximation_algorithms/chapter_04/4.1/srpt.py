import heapq
from operator import attrgetter
import random
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS as mc
from job import job


# Shortest Remaining Processing Time algorithm
class srpt():
    def __init__(self, jobs):
        self.jobs = sorted(jobs, key=attrgetter('rd', 'pt'))
        self.__do()

    def __stacking(self):
        if self.__i >= len(self.jobs):
            return

        if not self.__stack and self.__t < self.jobs[self.__i].rd:
            self.__t = self.jobs[self.__i].rd

        while self.__i < len(self.jobs) and self.jobs[self.__i].rd <= self.__t:
            heapq.heappush(self.__stack, self.jobs[self.__i])
            self.__i += 1

    def __print(self):
        print
        for j in self.jobs:
            print j

    def __do(self):
        self.__print()
        self.__t = 0
        self.__i = 0
        self.__stack = []
        while not self.__i == len(self.jobs):
            self.__stacking()
            while self.__stack:
                fin = float('inf')
                if self.__i < len(self.jobs):
                    fin = self.jobs[self.__i].rd + self.jobs[self.__i].pt
                li = self.__t + self.__stack[0].pt
                if fin < li:
                    j = heapq.heappop(self.__stack)
                    nj = self.jobs[self.__i]
                    j.ct.append([self.__t, nj.rd])
                    j.pt -= nj.rd - self.__t
                    heapq.heappush(self.__stack, j)
                    self.__t = nj.rd
                else:
                    j = heapq.heappop(self.__stack)
                    j.ct.append([self.__t, self.__t + j.pt])
                    self.__t += j.pt
                self.__stacking()
        self.__print()

    def draw(self, fname=None):
        for j in jobs:
            j.draw()
        plt.gca().set_ylim([0, 2])
        plt.gca().margins(0.1)
        if fname:
            plt.savefig(fname, bbox_inches='tight')
        else:
            plt.show()


if __name__ == '__main__':
    jobs = []
    c = mc.values()
    n = len(c) - 1
    random.seed(0)
    jobs.append(job(2, 0, c[random.randint(0, n)]))
    jobs.append(job(1, 4, c[random.randint(0, n)]))
    jobs.append(job(4, 1, c[random.randint(0, n)]))
    sched = srpt(jobs)
    for j in sched.jobs:
        print j.ct
    sched.draw('srpt_for_js1.png')
