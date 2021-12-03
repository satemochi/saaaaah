class furthest_in_future:
    def __init__(self, cache_size=3, access_sequence=None):
        if access_sequence:
            if cache_size < len(access_sequence):
                self.__sched(cache_size, access_sequence)

    def __sched(self, cache_size, access_sequence):
        self._evicted_elements = {}
        cache = {access_sequence[i] for i in range(cache_size)}
        for i in range(cache_size, len(access_sequence)):
            if access_sequence[i] in cache:
                continue
            cache.remove(e := self._to_be_evicted(i, cache, access_sequence))
            cache.add(access_sequence[i])
            self._evicted_elements[i] = e

    @staticmethod
    def _to_be_evicted(i, cache, sequence):
        a = {c: -t for t, c in enumerate(reversed(sequence[i+1:]+list(cache)))}
        return max((a[c], c) for c in cache)[1]

    @property
    def schedule(self):
        return self._evicted_elements


if __name__ == '__main__':
    print(f'cache size: {(cache_size := 6)}')
    ac = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 5, 4, 1, 2, 2, 1, 3, 4, 5, 1, 6, 1, 4]
    print(f'requests: {ac}')
    fif = furthest_in_future(cache_size=cache_size, access_sequence=ac)
    print(fif.schedule)
    print('cache miss count:', len(fif.schedule))
