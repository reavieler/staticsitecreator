import unittest

from main import *


class TestMain(unittest.TestCase):
    def test_eq(self):


        #text textnode test
        testNode1 = TextNode("texto de teste!!", "text")
        testNodeLeaf1 = text_node_to_html_node(testNode1)
        print(f"textnode: {testNodeLeaf1.__repr__()}")

        self.assertEqual(testNodeLeaf1.tag, None)
        self.assertEqual(testNodeLeaf1.value, 'texto de teste!!')
        self.assertEqual(testNodeLeaf1.children, None)
        self.assertEqual(testNodeLeaf1.props, None)

        #bold textnode test
        testNode2 = TextNode("texto de teste!!","bold")
        testNodeLeaf2 = text_node_to_html_node(testNode2)
        print(f"boldnode: {testNodeLeaf2.__repr__()}")

        self.assertEqual(testNodeLeaf2.tag, "b")
        self.assertEqual(testNodeLeaf2.value, 'texto de teste!!')
        self.assertEqual(testNodeLeaf2.children, None)
        self.assertEqual(testNodeLeaf2.props, None)

        #italic textnode test
        testNode3 = TextNode("texto de teste!!", "italic")
        testNodeLeaf3 = text_node_to_html_node(testNode3)
        print(f"italicnode: {testNodeLeaf3.__repr__()}")

        self.assertEqual(testNodeLeaf3.tag, "i")
        self.assertEqual(testNodeLeaf3.value, 'texto de teste!!')
        self.assertEqual(testNodeLeaf3.children, None)
        self.assertEqual(testNodeLeaf3.props, None)

        #code textnode test
        testNode4 = TextNode("texto de teste!!", "code")
        testNodeLeaf4 = text_node_to_html_node(testNode4)
        print(f"codenode: {testNodeLeaf4.__repr__()}")

        self.assertEqual(testNodeLeaf4.tag, "code")
        self.assertEqual(testNodeLeaf4.value, 'texto de teste!!')
        self.assertEqual(testNodeLeaf4.children, None)
        self.assertEqual(testNodeLeaf4.props, None)

        #link textnode test
        testNode5 = TextNode("texto de teste!!", "link", "https://www.google.com")
        testNodeLeaf5 = text_node_to_html_node(testNode5)
        print(f"linknode: {testNodeLeaf5.__repr__()}")

        self.assertEqual(testNodeLeaf5.tag, "a")
        self.assertEqual(testNodeLeaf5.value, 'texto de teste!!')
        self.assertEqual(testNodeLeaf5.children, None)
        self.assertEqual(testNodeLeaf5.props, {"href": "https://www.google.com"})

        #image textnode test
        testNode6 = TextNode("texto de teste!!", "image", "https://www.google.com")
        testNodeLeaf6 = text_node_to_html_node(testNode6)
        print(f"imagenode: {testNodeLeaf6.__repr__()}")

        self.assertEqual(testNodeLeaf6.tag, "img")
        self.assertEqual(testNodeLeaf6.value, '')
        self.assertEqual(testNodeLeaf6.children, None)
        self.assertEqual(testNodeLeaf6.props, {"src": "https://www.google.com", "alt": "texto de teste!!"})



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

