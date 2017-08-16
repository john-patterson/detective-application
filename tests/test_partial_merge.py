# -*- coding: utf-8 -*-
import unittest

from suplariapp.core import merge_testimonies


class PartialMergeCases(unittest.TestCase):
    def assertTest(self, in_file, expected):
        actual = merge_testimonies(in_file)
        actual.sort()
        expected.sort()
        self.assertEqual(actual, expected)

    def test_from_spec_1(self):
        test_data = [
            ['buying gas', 'pouring gas', 'laughing', 'lighting match', 'fire', 'smoke'],
            ['buying gas', 'pouring gas', 'crying', 'fire', 'smoke'],
        ]
        self.assertTest(test_data, [
            ['buying gas', 'pouring gas', 'laughing', 'lighting match', 'fire', 'smoke'],
            ['buying gas', 'pouring gas', 'crying', 'fire', 'smoke'],
        ])

    def test_from_spec_2(self):
        test_data = [
            ['shadowy figure', 'demands', 'scream', 'siren'],
            ['shadowy figure', 'pointed gun', 'scream'],
        ]
        self.assertTest(test_data, [
            ['shadowy figure', 'demands', 'scream', 'siren'],
            ['shadowy figure', 'pointed gun', 'scream', 'siren'],
        ])

    def test_long_divergence(self):
        self.assertTest([['a', 'b', 'c'], ['a', '1', '2', '3', '4', '5', '6', 'c', 'd']],
                        [['a', 'b', 'c', 'd'], ['a', '1', '2', '3', '4', '5', '6', 'c', 'd']])

    def test_simple(self):
        self.assertTest([['a', 'b', 'c'], ['a', 'd', 'c']],
                        [['a', 'b', 'c'], ['a', 'd', 'c']])

    def test_at_head(self):
        self.assertTest([['a', 'b', 'c'], ['d', 'b', 'c']],
                        [['a', 'b', 'c'], ['d', 'b', 'c']])

    def test_at_tail(self):
        self.assertTest([['a', 'b', 'c'], ['a', 'b', 'd']],
                        [['a', 'b', 'c'], ['a', 'b', 'd']])

    def test_with_one_unification(self):
        self.assertTest([['a', 'b', 'c', 'd', 'e'], ['a', 'b1', 'c', 'c2', 'd']],
                        [['a', 'b', 'c', 'c2', 'd', 'e'], ['a', 'b1', 'c', 'c2', 'd', 'e']])

    def test_multiple_divergence(self):
        self.assertTest([
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            ['e', '3', 'g'],
            ['a', '1', 'c'],
            ['c', '2', 'e'],
        ], [
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            ['a', '1', 'c', 'd', 'e', 'f', 'g'],
            ['a', 'b', 'c', '2', 'e', 'f', 'g'],
            ['a', 'b', 'c', 'd', 'e', '3', 'g'],
            ['a', 'b', 'c', '2', 'e', '3', 'g'],
            ['a', '1', 'c', 'd', 'e', '3', 'g'],
            ['a', '1', 'c', '2', 'e', 'f', 'g'],
            ['a', '1', 'c', '2', 'e', '3', 'g'],
        ])

    def test_graph_diverges_before_merge(self):
        """
        This test case encapsulates the following graph
                  *--*--*
                 /       \
                /  *------*----*
               /  /           /
          * - *--*           /
                  \         /
                   *-------*
        """
        test_data = [
            ['a', 'b', 'c', 'd', 'e', 'f'],
            ['b', 'c1', 'd1', 'e1', 'e'],
            ['c', 'd2', 'e2', 'f'],
        ]
        self.assertTest(test_data, [
            ['a', 'b', 'c1', 'd1', 'e1', 'e', 'f'],
            ['a', 'b', 'c', 'd', 'e', 'f'],
            ['a', 'b', 'c', 'd2', 'e2', 'f'],
        ])

    def test_graph_diverges_before_merge_never_converges(self):
        """
        This test case encapsulates the following graph
                  *--*--*
                 /       \
                /  *------*----*
               /  /
          * - *--*
                  \
                   *-------*
        """
        test_data = [
            ['a', 'b', 'c', 'd', 'e', 'f'],
            ['b', 'c1', 'd1', 'e1', 'e'],
            ['c', 'd2', 'e2'],
        ]
        self.assertTest(test_data, [
            ['a', 'b', 'c1', 'd1', 'e1', 'e', 'f'],
            ['a', 'b', 'c', 'd', 'e', 'f'],
            ['a', 'b', 'c', 'd2', 'e2'],
        ])

    def test_merging_at_branch_point(self):
        """
        This test case encapsulates the following graph
            b
         /     \
        a - c - f
        \      /
            d

        ---->

           1 ----- b
         /          \
        a - 2 - c - f
        \          /
         3 ------ d
        """

        test_data = [
            ['a', 'c', 'f'],
            ['a', 'b', 'f'],
            ['a', 'd', 'f'],
            ['a', '1', 'b'],
            ['a', '2', 'c'],
            ['a', '3', 'd'],
        ]
        self.assertTest(test_data, [
            ['a', '1', 'b', 'f'],
            ['a', '2', 'c', 'f'],
            ['a', '3', 'd', 'f'],
        ])

    def test_merging_at_converging_point(self):
        """
        This test case encapsulates the following graph
            b
         /     \
        a - c - f
        \      /
            d

        ---->

           b ----- 1
         /          \
        a - c - 2 - f
        \          /
         d ------ 3
        """

        test_data = [
            ['a', 'c', 'f'],
            ['a', 'b', 'f'],
            ['a', 'd', 'f'],
            ['b', '1', 'f'],
            ['c', '2', 'f'],
            ['d', '3', 'f'],
        ]
        self.assertTest(test_data, [
            ['a', 'b', '1', 'f'],
            ['a', 'c', '2', 'f'],
            ['a', 'd', '3', 'f'],
        ])

    def test_stress_algorithm(self):
        """
        This test case encapsulates the following graph
        c -> f -> i -> k -> m -> o
        ^ \   ^\   \        |   /
        |  \v    \  \----\v v  v
        b -> e -> h         p
        |  /^    /  /----/^ ^  ^
        v /   v/   /        |  \
        a -> b -> g -> j -> l -> n
        """

        test_data = [
            ['b', 'a', 'd', 'g', 'j', 'l', 'n'],
            ['b', 'c', 'f', 'i', 'k', 'm', 'o'],
            ['b', 'e', 'h', 'd'],
            ['b', 'e', 'h', 'f'],
            ['a', 'e'],
            ['c', 'e'],
            ['c', 'f', 'i', 'p'],
            ['k', 'm', 'p'],
            ['j', 'l', 'p'],
            ['a', 'd', 'g', 'p'],
            ['o', 'p'],
            ['n', 'p'],
            ['p', 'q'],
        ]
        self.assertTest(test_data, [
            ['b', 'c', 'f', 'i', 'k', 'm', 'o', 'p', 'q'],
            ['b', 'a', 'd', 'g', 'j', 'l', 'n', 'p', 'q'],
            ['b', 'a', 'd', 'g', 'j', 'l', 'p', 'q'],
            ['b', 'c', 'f', 'i', 'k', 'm', 'p', 'q'],
            ['b', 'c', 'f', 'i', 'p', 'q'],
            ['b', 'a', 'd', 'g', 'p', 'q'],
            ['b', 'e', 'h', 'd', 'g', 'j', 'l', 'n', 'p', 'q'],
            ['b', 'e', 'h', 'd', 'g', 'j', 'l', 'p', 'q'],
            ['b', 'e', 'h', 'd', 'g', 'p', 'q'],
            ['b', 'e', 'h', 'f', 'i', 'k', 'm', 'o', 'p', 'q'],
            ['b', 'e', 'h', 'f', 'i', 'k', 'm', 'p', 'q'],
            ['b', 'e', 'h', 'f', 'i', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'd', 'g', 'j', 'l', 'n', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'd', 'g', 'j', 'l', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'd', 'g', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'f', 'i', 'k', 'm', 'o', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'f', 'i', 'k', 'm', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'f', 'i', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'f', 'i', 'k', 'm', 'o', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'f', 'i', 'k', 'm', 'p', 'q'],
            ['b', 'a', 'e', 'h', 'f', 'i', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'd', 'g', 'j', 'l', 'n', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'd', 'g', 'j', 'l', 'p', 'q'],
            ['b', 'c', 'e', 'h', 'd', 'g', 'p', 'q'],
        ])

    def test_unicode(self):
        """
        Unicode compatibility test
        These emojis were chosen specifically because they have a tendency to break unicode unaware algorithms as they
        specify the bitmap plane higher than BMP (the SMP plane), so they require 4 bytes to specify.
        Algorithms that do not account for SMP characters usually end up in the middle of a byte ligature on these.
        For instance, the JetBrains editor I am using currently breaks on backspace through one of these characters. :)
        """
        test_data = [
            ['😿', '🙉'],
            ['🙈', '🙉', '🙊'],
        ]
        self.assertTest(test_data, [
            ['😿', '🙉', '🙊'],
            ['🙈', '🙉', '🙊'],
        ])


