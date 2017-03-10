import operator
from random import randint, seed
import matplotlib.pyplot as plt


class job:
    def __init__(self, processing_unit_time, release_date, due_date,
                 start_time=None, complete_time=None):
        self.pt = processing_unit_time
        self.rd = release_date
        self.dd = due_date
        self.st = start_time
        self.ct = complete_time

    def lateness(self):
        assert self.ct is not None, "lateness: 'complete_time' is None."
        return self.ct - self.dd

    def is_available(self, current_time):
        return True if self.rd <= current_time else False

    def draw(self):
        assert self.st is not None, "draw: 'start_time' is None."
        return plt.Rectangle((self.st, 0), self.pt, 0.2, alpha=0.25)

    def __str__(self):
        return '(pt: ' + str(self.pt) + ', rd: ' + str(self.rd) + \
               ', dd: ' + str(self.dd) + ', ct: ' + str(self.ct) + ')'


def gen(n, s=1):
    seed(s)
    return [job(randint(1, 9), randint(1, 9), -randint(1, 9))
            for i in range(n)]


def earliest_due_date(jobs):
    t = min(j.rd for j in jobs)
    counter = len(jobs)
    jobs.sort(key=operator.attrgetter('dd'))
    while counter > 0:
        for i in range(len(jobs)):
            if jobs[i].ct is not None or not jobs[i].is_available(t):
                if i == len(jobs) - 1:
                    t = min(j.rd for j in jobs if t < j.rd)
                continue
            jobs[i].st = t
            t += jobs[i].pt
            jobs[i].ct = t
            counter -= 1
            break
    return max(j.lateness() for j in jobs)


if __name__ == '__main__':
    jobs = gen(5, 5)
    print [str(j) for j in jobs]
    print 'lateness:', earliest_due_date(jobs)
    print [str(j) for j in jobs]

    for i in range(len(jobs)):
        plt.gca().add_patch(jobs[i].draw())
    plt.gca().set_ylim([0, 3])
    plt.gca().margins(0.1)
    plt.show()
