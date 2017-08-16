import unittest

from suplariapp.utilities import TestimonyGraph


class TestimonyIteratorTests(unittest.TestCase):
    def test_empty_graph_empty_vertexes(self):
        g = TestimonyGraph()
        self.assertEqual(set(), g.vertexes)
        self.assertFalse(g.has_vertex('a'))

    def test_add_edge_vertex_list_updates(self):
        g = TestimonyGraph()
        g['a'] = ['b', 'c']
        self.assertEqual({'a', 'b', 'c'}, g.vertexes)
        self.assertTrue(g.has_vertex('a'))
        self.assertTrue(g.has_vertex('b'))
        self.assertTrue(g.has_vertex('c'))

    def test_get_starting_points_empty_graph_empty(self):
        g = TestimonyGraph()
        self.assertEqual([], g.get_starting_points())

    def test_get_starting_points_with_single_start(self):
        g = TestimonyGraph()
        g['a'] = ['b']
        g['b'] = ['c', 'd']
        self.assertEqual(['a'], g.get_starting_points())

    def test_get_starting_points_with_multiple_starts(self):
        g = TestimonyGraph()
        g['a'] = ['b']
        g['b'] = ['c', 'd']
        g['e'] = ['f']
        g['g'] = ['c']
        self.assertEqual(['a', 'e', 'g'], sorted(g.get_starting_points()))

    def test_get_starting_points_no_start_but_nonempty(self):
        # Should be impossible, but best to not go on forever
        g = TestimonyGraph()
        g['a'] = ['b']
        g['b'] = ['a']
        self.assertEqual([], g.get_starting_points())

    def test_to_array_with_empty_graph_gives_empty_list(self):
        g = TestimonyGraph()
        self.assertEqual([], g.to_array())

    def test_to_array_no_branching(self):
        g = TestimonyGraph()
        g['a'], g['b'] = ['b'], ['c']
        self.assertEqual([['a', 'b', 'c']], g.to_array())

    def test_to_array_with_branching(self):
        g = TestimonyGraph()
        g['a'], g['b'] = ['b'], ['c', 'd']
        expected = sorted([['a', 'b', 'c'], ['a', 'b', 'd']])
        self.assertEqual(expected, sorted(g.to_array()))

    def test_to_array_with_cycle(self):
        # Should be impossible, but best to not go on forever
        g = TestimonyGraph()
        g['a'] = ['b']
        g['b'] = ['a']
        self.assertEqual([], sorted(g.to_array()))

