# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

"""
Test translator module on three algorithms: cat, hello, prob5
"""

import unittest
from tempfile import NamedTemporaryFile

import translator


class TranslatorTest(unittest.TestCase):
    def assert_equal_output(self, source: str, snapshot_filename: str):
        with NamedTemporaryFile() as temp:
            translator.main([source, temp.name])

            with open(source, encoding="utf-8") as file:
                result = file.read()
            with open(snapshot_filename, encoding="utf-8") as file:
                snapshot = file.read()

            self.assertEqual(result, snapshot)

    def test_cat_translation(self):
        source: str = "test/in/test_cat.asm"
        snap_out: str = "test/out/test_cat"

        self.assert_equal_output(source, snap_out)

    def test_hello_translation(self):
        source: str = "test/in/test_hello.asm"
        snap_out: str = "test/out/test_hello"

        self.assert_equal_output(source, snap_out)

    def test_prob5_translation(self):
        source: str = "test/in/test_pron5.asm"
        snap_out: str = "test/out/test_prob5"

        self.assert_equal_output(source, snap_out)
