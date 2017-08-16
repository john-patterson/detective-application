# -*- coding: utf-8 -*-
import unittest

from suplariapp.core import merge_testimonies


class FullMergeCases(unittest.TestCase):
    def assertTest(self, in_file, expected):
        actual = merge_testimonies(in_file)
        self.assertEqual(actual, expected)

    def test_empty_input(self):
        self.assertTest([], [])

    def test_single_testimony(self):
        self.assertTest([['a', 'b', 'c']],
                        [['a', 'b', 'c']])

    def test_simple_merge(self):
        self.assertTest([['a', 'b', 'c'], ['b', 'd', 'c']],
                        [['a', 'b', 'd', 'c']])

    def test_head_merge(self):
        self.assertTest([['a', 'b', 'c'], ['d', 'e', 'a']],
                        [['d', 'e', 'a', 'b', 'c']])

    def test_tail_merge(self):
        self.assertTest([['a', 'b', 'c'], ['c', 'e', 'o']],
                        [['a', 'b', 'c', 'e', 'o']])

    def test_from_spec_1(self):
        test_data = [
            ['shouting', 'fight', 'fleeing'],
            ['fight', 'gunshot', 'panic', 'fleeing'],
            ['anger', 'shouting'],
        ]
        self.assertTest(test_data,
                        [['anger', 'shouting', 'fight', 'gunshot', 'panic', 'fleeing']])

    def test_from_spec_2(self):
        test_data = [
            ['fight', 'gunshot', 'fleeing'],
            ['gunshot', 'falling', 'fleeing'],
        ]
        self.assertTest(test_data,
                        [['fight', 'gunshot', 'falling', 'fleeing']])

    def test_unicode(self):
        """
        Unicode compatibility test
        These emojis were chosen specifically because they have a tendency to break unicode unaware algorithms as they
        specify the bitmap plane higher than BMP (the SMP plane), so they require 4 bytes to specify.
        Algorithms that do not account for SMP characters usually end up in the middle of a byte ligature on these.
        For instance, the JetBrains editor I am using currently breaks on backspace through one of these characters. :)
        """
        test_data = [
            ['🙈', '🙉', '🙊'],
            ['🙈', '😿', '🙉'],
        ]
        self.assertTest(test_data, [['🙈', '😿', '🙉', '🙊']])
