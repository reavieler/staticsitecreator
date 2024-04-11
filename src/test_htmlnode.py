import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        leaf1 = LeafNode("p", "This is a paragraph of text.")
        leaf2 = LeafNode("a", "Click me!",None,{"href": "https://www.google.com"})
        leaf3 = LeafNode(None, 'texto de teste!!', None, None)

        # print(leaf1.__repr__())
        # print(leaf2.__repr__())
        self.assertEqual(leaf3.tag, None)
        self.assertEqual(leaf3.value, 'texto de teste!!')
        self.assertEqual(leaf3.children, None)
        self.assertEqual(leaf3.props, None)
        # self.assertEqual(leaf1.value, 'This is a paragraph of text.')
        # self.assertIsNone(leaf1.children, "LeafNodes should not have children classes associated.")
        # self.assertEqual(leaf1.to_html(), "<p>This is a paragraph of text.</p>")


        # print(leaf2.to_html())


        # node = ParentNode(
        #     "p",None,
        #     [
        #         LeafNode("b", "Bold text"),
        #         LeafNode(None, "Normal text"),
        #         LeafNode("i", "italic text"),
        #         LeafNode(None, "Normal text"),
        #     ],
        # )

        # print(node.__repr__())

        # print(node.to_html())


if __name__ == "__main__":
    unittest.main()

