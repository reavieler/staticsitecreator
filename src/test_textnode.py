import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold","https://www.youtube.com")
        node2 = TextNode("This is a text node", "bold","https://www.youtube.com")
        return self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

