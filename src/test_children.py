import unittest
from splitter import text_to_children

class TestTextToChildren(unittest.TestCase):
    def test_basic_text(self):
        result = text_to_children("Hello, world!")
        print("Basic text result:", result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tag, "")
        self.assertEqual(result[0].value, "Hello, world!")

    def test_bold_text(self):
        result = text_to_children("Hello, **world**!")
        print("Bold text result:", result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].tag, "b")
        self.assertEqual(result[1].value, "world")

    def test_italic_text(self):
        result = text_to_children("Hello, *world*!")
        print("Italic text result:", result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].tag, "i")
        self.assertEqual(result[1].value, "world")