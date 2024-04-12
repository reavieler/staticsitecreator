from textnode import *
from htmlnode import *

text_types = ["text", "bold", "italic", "code", "link", "image"]
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"



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


def split_nodes_delimiter(old_nodes, delimiter, texttype):
    nodesoutput = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodesoutput.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0 or node.text.count(delimiter) == 0:
                raise ValueError("Invalid Markdown syntax! Every delimiter should be accompanied by a closing delimiter.")
            node_split_by_delimiter = node.text.split(delimiter)
            print(node_split_by_delimiter)
            for i in range(len(node_split_by_delimiter)):
                if i % 2 == 0:
                    nodesoutput.append(TextNode(node_split_by_delimiter[i], text_type_text))
                else:
                    nodesoutput.append(TextNode(node_split_by_delimiter[i], texttype))

    print(nodesoutput)
    return nodesoutput

def main():
    
    node = TextNode("This is text with a **bold!!!** word", text_type_text)
    new_nodes = split_nodes_delimiter([node],"**",text_type_bold)
    print(new_nodes)

main()


#git commit -m "added split_nodes_delimiter. It creates new text nodes based on textnodes that have markdown type language"