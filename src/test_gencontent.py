import unittest

from gencontent import extract_title

class TestGencontent(unittest.TestCase):
    def test_extract_title(self):
        test_title = extract_title("# This is an h1 header")
        result_title = "This is an h1 header"
        print(result_title)
        self.assertEqual(test_title, result_title)
