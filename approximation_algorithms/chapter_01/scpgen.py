import math
import random
import sys


class scpgen:
    """ Random test instance generator for ``SET COVER'' problems

        ref.)
            https://sites.google.com/site/shunjiumetani/benchmark

    """
    def __init__(self, cvr_num, var_num, density, seed=0):
        self.covering_set_num = cvr_num
        self.universal_set_size = var_num
        self.density = density
        self.__set_seed(seed)
        self.cost = self.__set_cost()
        self.sets, self.sizes = self.__gen_instance()

    def __set_seed(self, seed):
        random.seed(seed)

    def __set_cost(self):
        return sorted([random.randint(1, 100)
                       for i in range(self.covering_set_num)])

    def __preprocess(self):
        el_num = int(math.ceil(self.covering_set_num *
                               self.universal_set_size * self.density))
        x = []
        for i in range(self.covering_set_num):
            x.append(i)
            x.append(i)
        var_idx_cvr = []
        var_idx_cvr.append(x)
        var_num_cvr = [0] * self.covering_set_num
        for h in range(len(x), el_num):
            var_idx_cvr[0].append(random.randint(0, self.covering_set_num - 1))
            var_num_cvr[var_idx_cvr[0][-1]] += 1
        for i in range(1, self.covering_set_num):
            var_idx_cvr.append(var_idx_cvr[i-1][var_num_cvr[i-1]:])

        scan_ptr = [0] * self.covering_set_num
        h, j = 0, 0
        while j < self.universal_set_size and h < el_num:
            i = h % self.covering_set_num
            if scan_ptr[i] < var_num_cvr[i]:
                var_idx_cvr[i][scan_ptr[i]] = j
                scan_ptr[i] += 1
                j += 1
            h += 1
        if j < self.universal_set_size and h >= el_num:
            raise

        return (var_idx_cvr, var_num_cvr, scan_ptr)

    def __gen_instance(self):
        try:
            var_idx_cvr, var_num_cvr, scan_ptr = self.__preprocess()
        except:
            print "Fail to generate instance...\n\
Incorrect settings might be occcured on parameters.\n"
            sys.exit(1)

        for i in range(self.covering_set_num):
            temp_array = range(self.universal_set_size)
            for h in range(scan_ptr[i]):
                temp_array[var_idx_cvr[i][h]] = -1
            array = []
            for j in range(self.universal_set_size):
                if temp_array[j] != -1:
                    array.append(temp_array[j])
            random.shuffle(array)
            for h in range(scan_ptr[i], var_num_cvr[i]):
                var_idx_cvr[i][h] = array[h]
            var_idx_cvr[i] = sorted(var_idx_cvr[i][:var_num_cvr[i]])

        return (var_idx_cvr, var_num_cvr)

    def __str__(self):
        s = "\nNumber of subsets for instance: "
        s += str(self.covering_set_num) + "\n"
        s += "The domain of each subset: [1, "
        s += str(self.universal_set_size) + "]\n"
        s += "The cost of each subsets: "
        s += " ".join([str(c) for c in self.cost]) + "\n\n"
        for i in range(self.covering_set_num):
            elems = [str(self.sets[i][h]+1) for h in range(self.sizes[i])]
            s += "SUBSET " + str(i) + ": size("
            s += str(self.sizes[i]) + ")\n" + " ".join(elems) + "\n\n"
        return s

    def __is_contained(self, ith_subset, elem):
        return 0 if elem not in self.sets[ith_subset] else 1

    def __get_vector(self, elem):
        return [self.__is_contained(ith_subset, elem)
                for ith_subset in range(self.covering_set_num)]

    def get_rows(self):
        for elem in range(self.universal_set_size):
            yield self.__get_vector(elem)

    def get_f(self):
        fi = [0] * (self.universal_set_size)
        for i in range(self.covering_set_num):
            for elem in self.sets[i]:
                fi[elem] += 1
        return (fi.index(max(fi))+1, max(fi))

    def is_covered(self, I):
        u = set([])
        for idx in I:
            u = u | set(self.sets[idx])
        return list(u) == range(self.universal_set_size)


if __name__ == '__main__':
    scp_gen = scpgen(10, 100, 0.5, 3)
    print scp_gen
