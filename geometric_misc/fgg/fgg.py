class fgg():
    """A simple flip graph generator"""

    def __init__(self, n=6):
        self._vertex_count = 0
        self._polygon_vertex_count = n
        self._vertices = []
        self._dss_id_ref_tab = {}
        self._edges = []

    def get_vertex_count(self):
        return self._vertex_count

    def get_polygon_vertex_count(self):
        return self._polygon_vertex_count

    def get_init_dss(self):
        dss = unichr(0)
        for i in range(1, self._polygon_vertex_count - 1):
            dss += unichr(i) + unichr(0)
        return dss

    def print_dss(self, dss):
        return ''.join([str(ord(s)) for s in dss])

    def split(self, dss):
        split_strings = []
        head = 0
        for i in range(1, self._polygon_vertex_count - 1):
            tail = head
            while dss[tail] != unichr(i):
                tail += 1
            split_strings.append(dss[head: tail])
            head = tail
        split_strings.append(dss[head:])
        return split_strings

    def concatenate(self, splits, s1, pos1, s2, pos2):
        concat_string = ""
        for i in range(0, pos1):
            concat_string = concat_string + splits[i]
        concat_string = concat_string + s1
        for i in range(pos1 + 1, pos2):
            concat_string = concat_string + splits[i]
        concat_string = concat_string + s2
        for i in range(pos2 + 1, len(splits)):
            concat_string = concat_string + splits[i]
        return concat_string

    def del_char(self, s, i):
        return s[:i] + s[i+1:]

    def insert_char(self, s, i, c):
        return s[:i] + c + s[i:]

    def neighbor_dss_from_not_last_word(self, split_strings,
                                        ith_dec_seq, jth_word):
        s1 = self.del_char(split_strings[ith_dec_seq], jth_word)

        pred = split_strings[ith_dec_seq][jth_word - 1]
        succ = split_strings[ith_dec_seq][jth_word + 1]
        s2 = split_strings[ord(pred) - 1]

        for pos in range(0, len(s2)):
            if ord(s2[pos]) < ord(succ):
                s2 = self.insert_char(s2, pos, succ)
                break
            if pos == len(s2) - 1:
                s2 = s2 + succ
                break
        return self.concatenate(split_strings,
                                s2, ord(pred) - 1, s1, ith_dec_seq)

    def neighbor_dss_from_last_word(self, split_strings,
                                    ith_dec_seq, jth_word):
        s1 = self.del_char(split_strings[ith_dec_seq], jth_word)

        c = split_strings[ith_dec_seq][jth_word - 1]
        s2 = ""
        swap_pos2 = 0
        for swap_pos2 in range(ith_dec_seq + 1, len(split_strings)):
            target_char = split_strings[ith_dec_seq][jth_word]
            pos = split_strings[swap_pos2].find(target_char)
            if pos == -1:
                continue
            else:
                s2 = self.insert_char(split_strings[swap_pos2], pos, c)
                break
        return self.concatenate(split_strings, s1, ith_dec_seq, s2, swap_pos2)

    def get_neighbors(self, dss):
        S = []
        splits = self.split(dss)
        for i in range(1, len(splits) - 1):
            if len(splits[i]) == 1:
                continue
            for j in range(1, len(splits[i]) - 2):
                S.append(self.neighbor_dss_from_not_last_word(splits, i, j))
            if i != len(splits) - 1:
                S.append(self.neighbor_dss_from_last_word(splits, i,
                                                          len(splits[i]) - 1))
        return S

    def gen(self):
        if self._polygon_vertex_count < 3:
            return
        init_dss = self.get_init_dss()
        self._vertices.append(init_dss)
        self._dss_id_ref_tab[init_dss] = 0
        self._vertex_count = 1

        task_stack = [init_dss]
        while task_stack:
            dss = task_stack.pop()
            neighbors = self.get_neighbors(dss)

            for s in neighbors:
                if s not in self._vertices:
                    self._vertices.append(s)
                    self._dss_id_ref_tab[s] = self._vertex_count
                    self._vertex_count += 1
                    task_stack.append(s)

                did, sid = self._dss_id_ref_tab[dss], self._dss_id_ref_tab[s]
                e = (did, sid) if did < sid else (sid, did)
                if e not in self._edges:
                    self._edges.append(e)

    def get_vertices(self):
        return self._vertices

    def get_edges(self):
        return self._edges

    def get_ref_table(self):
        return self._dss_id_ref_tab

    def get_triangulation_edges(self, vid):
        s = self._vertices[vid]
        t_edges = []
        si = 0
        for i in range(1, self._polygon_vertex_count):
            while si < len(s):
                if ord(s[si]) == i:
                    break
                t_edges.append((i, ord(s[si])))
                si += 1
        return t_edges
