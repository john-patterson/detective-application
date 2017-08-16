import unittest

from suplariapp.utilities import Testimony


def get_iterator(data):
    return Testimony(data).get_iterator()


class TestimonyIteratorTests(unittest.TestCase):
    def test_empty_data_all_values_none(self):
        it = get_iterator([])
        self.assertIsNone(it.value())
        self.assertIsNone(it.next())
        self.assertIsNone(it.peek_next())

    def test_none_data_all_values_none(self):
        it = get_iterator(None)
        self.assertIsNone(it.value())
        self.assertIsNone(it.next())
        self.assertIsNone(it.peek_next())

    def test_iterate_off_end_all_values_none(self):
        it = get_iterator([1, 2])
        self.assertEqual(1, it.value())
        self.assertEqual(2, it.peek_next())
        self.assertEqual(2, it.next())
        self.assertEqual(2, it.value())
        self.assertIsNone(it.peek_next())
        self.assertIsNone(it.next())
        self.assertIsNone(it.peek_next())
        self.assertIsNone(it.next())
