import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        leaf1 = LeafNode("p", "This is a paragraph of text.")
        leaf2 = LeafNode("a", "Click me!",None,{"href": "https://www.google.com"})

        print(leaf1.__repr__())
        print(leaf2.__repr__())
        self.assertEqual(leaf1.tag, 'p')
        self.assertEqual(leaf1.value, 'This is a paragraph of text.')
        self.assertIsNone(leaf1.children, "LeafNodes should not have children classes associated.")
        self.assertEqual(leaf1.to_html(), "<p>This is a paragraph of text.</p>")


        print(leaf2.to_html())


if __name__ == "__main__":
    unittest.main()

