import unittest

from gen_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_et_basic(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_et_double(self):
        actual = extract_title(
            """
# This is a title
# This is an ignored title
""")
        self.assertEqual(actual, "This is a title")

    def test_et_extra(self):
        actual = extract_title(
            """
# This is a title
This is not a title.
!This is also not a title.
* Still not a title
* Also not a title
Print Hello World
        """)
        self.assertEqual(actual, "This is a title")

    def test_et_mal(self):
        try:
            extract_title("##malformed title")
            self.fail("malformed title")
        except Exception as e:
            pass

    def test_et_none(self):
        try:
            extract_title("No title found")
            self.fail("Not a title")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()