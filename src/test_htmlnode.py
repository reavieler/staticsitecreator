import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode(tag = 'p', value = 'This is a paragraph of text.')
        print(leaf.__repr__())
        self.assertEqual(leaf.tag, 'p')
        #self.assertEqual(leaf.value, 'This is a paragraph of text.')
        # `children` should be None for a LeafNode; verify that as well
        self.assertIsNone(leaf.children)
        # If `props` was not provided, it should be None or an empty dictionary based on your design
        self.assertIsNone(leaf.props, "Props should be None or an empty dictionary by default.")




if __name__ == "__main__":
    unittest.main()

