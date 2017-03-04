import fgg
import unittest


class FggTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(FggTest, self).__init__(*args, **kwargs)
        self.catalan_num = [0, 0, 0, 1, 2, 5, 14, 42, 132, 429,
                            1430, 4862, 16796, 58786]
        self.edge_num = [0, 0, 0, 0, 1, 5, 21, 84, 330, 1287,
                         5005, 19448, 75582, 293930]

    def test_constractor(self):
        f = fgg.fgg()
        vc = f.get_vertex_count()
        pvc = f.get_polygon_vertex_count()
        self.assertEqual(0, vc)
        self.assertEqual(6, pvc)

    def test_get_init_dss(self):
        f = fgg.fgg()
        dss = unichr(0) + unichr(1) + unichr(0) + unichr(2) + unichr(0)
        dss += unichr(3) + unichr(0) + unichr(4) + unichr(0)
        self.assertEqual(dss, f.get_init_dss())
        self.assertEqual(2 * f.get_polygon_vertex_count() - 3,
                         len(f.get_init_dss()))

    def test_print_dss(self):
        f = fgg.fgg()
        dss = "010203040"
        self.assertEqual(dss, f.print_dss(f.get_init_dss()))

    def test_split(self):
        f = fgg.fgg()
        split_strings = [unichr(0), unichr(1) + unichr(0),
                         unichr(2) + unichr(0), unichr(3) + unichr(0),
                         unichr(4) + unichr(0)]
        self.assertEqual([unicode(x) for x in split_strings],
                         f.split(f.get_init_dss()))

    def test_del_char(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        dec_seq = map(lambda x: f.print_dss(x), f.split(init_dss))
        ans = '1'
        self.assertEqual(ans, f.del_char(dec_seq[1], 1))
        ans = '0'
        self.assertEqual(ans, f.del_char(dec_seq[3], 0))

    def test_insert_char(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        dec_seq = map(lambda x: f.print_dss(x), f.split(init_dss))
        ans = "109"
        self.assertEqual(ans, f.insert_char(dec_seq[1], 2, '9'))
        ans = "290"
        self.assertEqual(ans, f.insert_char(dec_seq[2], 1, '9'))
        ans = "930"
        self.assertEqual(ans, f.insert_char(dec_seq[3], 0, '9'))

    def test_concatenate(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        dec_seq = map(lambda x: f.print_dss(x), f.split(init_dss))
        ans = "0a20b40"
        self.assertEqual(ans, f.concatenate(dec_seq, "a", 1, "b", 3))
        ans = "0xy3040"
        self.assertEqual(ans, f.concatenate(dec_seq, "x", 1, "y", 2))
        ans = "a102030b"
        self.assertEqual(ans, f.concatenate(dec_seq, "a", 0, "b", 4))

    def test_neighbor_dss_from_last_word(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        splits = f.split(init_dss)
        ndss = f.neighbor_dss_from_last_word(splits, 1, 1)
        ans = "012103040"
        self.assertEqual(ans, f.print_dss(ndss))
        ndss = f.neighbor_dss_from_last_word(splits, 2, 1)
        ans = "010232040"
        self.assertEqual(ans, f.print_dss(ndss))
        ndss = f.neighbor_dss_from_last_word(splits, 3, 1)
        ans = "010203430"
        self.assertEqual(ans, f.print_dss(ndss))

    def test_neighbor_dss_from_not_last_word(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        splits = f.split(init_dss)

        ndss = f.neighbor_dss_from_last_word(splits, 1, 1)
        splits = f.split(ndss)
        ndss = f.neighbor_dss_from_not_last_word(splits, 2, 1)
        ans = "010203040"
        self.assertEqual(ans, f.print_dss(ndss))

        splits = f.split(init_dss)
        ndss = f.neighbor_dss_from_last_word(splits, 2, 1)
        splits = f.split(ndss)
        ndss = f.neighbor_dss_from_not_last_word(splits, 3, 1)
        self.assertEqual(ans, f.print_dss(ndss))

        splits = f.split(init_dss)
        ndss = f.neighbor_dss_from_last_word(splits, 3, 1)
        splits = f.split(ndss)
        ndss = f.neighbor_dss_from_not_last_word(splits, 4, 1)
        self.assertEqual(ans, f.print_dss(ndss))

    def test_get_neighbors(self):
        f = fgg.fgg()
        init_dss = f.get_init_dss()
        ans = ["012103040", "010232040", "010203430"]
        self.assertEqual(ans, map(lambda x: f.print_dss(x),
                                  f.get_neighbors(init_dss)))

    def test_gen_2(self):
        n = 2
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_3(self):
        n = 3
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_4(self):
        n = 4
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_5(self):
        n = 5
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_6(self):
        n = 6
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_7(self):
        n = 7
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_8(self):
        n = 8
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_9(self):
        n = 9
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_10(self):
        n = 10
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_gen_11(self):
        n = 11
        f = fgg.fgg(n)
        f.gen()
        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
        self.assertEqual(self.edge_num[n], len(f.get_edges()))

# Because of elapsed time, omitting, then commented out.
#    def test_gen_12(self):
#        n = 12
#        f = fgg.fgg(n)
#        f.gen()
#        self.assertEqual(self.catalan_num[n], len(f.get_vertices()))
#        self.assertEqual(self.catalan_num[n], len(f.get_ref_table()))
#        self.assertEqual(self.edge_num[n], len(f.get_edges()))

    def test_get_triangulation_edges(self):
        f = fgg.fgg()
        f.gen()
        ans = [(1, 0), (2, 1), (2, 0), (3, 2), (3, 0),
               (4, 3), (4, 0), (5, 4), (5, 0)]
        self.assertEqual(ans, f.get_triangulation_edges(0))
        ans = [(1, 0), (2, 1), (2, 0), (3, 2), (4, 3),
               (4, 2), (4, 0), (5, 4), (5, 0)]
        self.assertEqual(ans, f.get_triangulation_edges(2))


if __name__ == '__main__':
    unittest.main()
