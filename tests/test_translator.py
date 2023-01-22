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
        source: str = "in/cat.asm"
        snap_out: str = "out/cat"

        self.assert_equal_output(source, snap_out)

    def test_hello_translation(self):
        source: str = "in/hello.asm"
        snap_out: str = "out/hello"

        self.assert_equal_output(source, snap_out)

    def test_prob5_translation(self):
        source: str = "in/prob5.asm"
        snap_out: str = "out/prob5"

        self.assert_equal_output(source, snap_out)
