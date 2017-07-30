from operator import attrgetter
import heapq
import unittest
from job import job
from srpt import srpt

class test_jobs(unittest.TestCase):

    def test_regal_create(self):
        j = job(1, 0)
        self.assertEqual(j.pt, 1)
        self.assertEqual(j.rd, 0)
        j = job()
        self.assertEqual(j.pt, 1)
        self.assertEqual(j.rd, 0)
        s = 'pt: 1, rd: 0'
        self.assertEqual(str(j), s)

    def test_irregal_create(self):
        pt_error_string = 'pt must be greater than zero'
        with self.assertRaises(AssertionError) as context:
            job(0, 0)
        self.assertTrue(pt_error_string in context.exception)

        rd_error_string = 'rd must be greater than or equal to zero.'
        with self.assertRaises(AssertionError) as context:
            job(1, -1)
        self.assertTrue(rd_error_string in context.exception)

        pt_int_error_string = 'pt must be int'
        with self.assertRaises(AssertionError) as context:
            job(1.1, 0)
        self.assertTrue(pt_int_error_string in context.exception)

        rd_int_error_string = 'rd must be int'
        with self.assertRaises(AssertionError) as context:
            job(1, 0.2)
        self.assertTrue(rd_int_error_string in context.exception)

    def test_sorting(self):
        ref_jobs = [job(1, 0), job(2, 1), job(3, 1), job(4, 5)]
        jobs = []
        jobs.append(job(3, 1))
        jobs.append(job(1, 0))
        jobs.append(job(4, 5))
        jobs.append(job(2, 1))
#        jobs.sort()
        for r, t in zip(ref_jobs, sorted(jobs, key=attrgetter('rd', 'pt'))):
            self.assertEqual(r, t)

    def test_heapq(self):
        ref_jobs = [job(1, 0), job(1, 3), job(2, 1), job(3, 1), job(4, 5)]
        target_jobs = []
        heapq.heappush(target_jobs, job(1, 3))
        heapq.heappush(target_jobs, job(3, 1))
        heapq.heappush(target_jobs, job(1, 0))
        heapq.heappush(target_jobs, job(4, 5))
        heapq.heappush(target_jobs, job(2, 1))
        for i in range(len(target_jobs)):
            self.assertEqual(ref_jobs[i], heapq.heappop(target_jobs))

    def test_srpt_text_jobs(self):
        jobs = [job(2, 0), job(1, 4), job(4, 1)]
        ref = [[[0, 2]], [[2, 4], [5, 7]], [[4, 5]]]
        sched = srpt(jobs)
        for i, j in enumerate(sched.jobs):
            self.assertEqual(j.ct, ref[i])

    def test_srpt_1(self):
        jobs = [job(1, 1), job(1, 4), job(4, 1)]
        ref = [[[1, 2]], [[2, 4], [5, 7]], [[4, 5]]]
        sched = srpt(jobs)
        for i, j in enumerate(sched.jobs):
            self.assertEqual(j.ct, ref[i])

    def test_srpt_2(self):
        jobs = [job(2, 1), job(1, 4), job(4, 1)]
        ref = [[[1, 3]], [[3, 4], [5, 8]], [[4, 5]]]
        sched = srpt(jobs)
        for i, j in enumerate(sched.jobs):
            self.assertEqual(j.ct, ref[i])


if __name__ == '__main__':
    unittest.main()
