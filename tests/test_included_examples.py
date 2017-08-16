import unittest
import json
import os

from suplariapp.core import merge_testimonies


class IncludedExamplesTests(unittest.TestCase):
    def get_input(self, file_name):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, file_name)
        json_data = None
        with open(file_path) as in_file:
            json_data = json.load(in_file)
        return json_data

    def assertTest(self, file_name, expected):
        json_data = self.get_input(file_name)
        actual = merge_testimonies(json_data)
        actual.sort()
        expected.sort()
        self.assertEqual(actual, expected)

    def test_example1(self):
        self.assertTest("example1.json", [
            ['fight', 'gunshot', 'falling', 'fleeing'],
        ])

    def test_example2(self):
        self.assertTest("example2.json", [
            ["shadowy figure", "demands", "scream", "siren"],
            ["shadowy figure", "pointed gun", "scream", "siren"],
        ])

    def test_example3(self):
        data = self.get_input("example3.json")
        actual = merge_testimonies(data)
        self.assertIs(data, actual)

    def test_example4(self):
        self.assertTest("example4.json", [
            ['0', '3'],
            ['0', '2', '3'],
            ['0', '1', '3'],
            ['0', '1', '2', '3'],
        ])
