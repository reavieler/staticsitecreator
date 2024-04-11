from textnode import *
from htmlnode import *

text_types = ["text", "bold", "italic", "code", "link", "image"]




def text_node_to_html_node(text_node):
    if text_node.text_type not in text_types:
        raise Exception("Not a valid text node!")
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, None, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", None, {"src": text_node.url, "alt": text_node.text})




def main():
    
    new_text_node = TextNode("texto de teste!!","text")
    text_node_to_html_node(new_text_node)

main()
