# -*- coding: utf-8 -*-
import unittest

from suplariapp.core import merge_testimonies


class DoNotMergeCases(unittest.TestCase):
    def assertTest(self, in_file):
        actual = merge_testimonies(in_file)
        self.assertIs(actual, in_file)

    def test_from_spec_1(self):
        test_data = [
            ['argument', 'stuff', 'pointing'],
            ['press brief', 'scandal', 'pointing'],
            ['bribe', 'coverup'],
        ]
        self.assertTest(test_data)

    def test_disjoint(self):
        test_data = [
            ['a', 'b', 'c'],
            ['1', '2', '3'],
            ['@', '$', '%'],
        ]
        self.assertTest(test_data)

    def test_one_common(self):
        test_data = [
            ['1', 'b', 'c'],
            ['1', '2', '3'],
            ['1', '$', '%'],
        ]
        self.assertTest(test_data)

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
            ['😾', '😿', '🙀'],
        ]
        self.assertTest(test_data)
