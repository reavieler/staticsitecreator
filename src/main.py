from textnode import *
from htmlnode import *
import re

text_types = ["text", "bold", "italic", "code", "link", "image"]
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
# possible_type_dict = {
#     "text":"",
#     "bold": "**",
#     "italic": "*",
#     "code": "`"
# }



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
            if node.text.count(delimiter) % 2 != 0:# or node.text.count(delimiter) == 0:
                raise ValueError("Invalid Markdown syntax! Every delimiter should be accompanied by a closing delimiter.")
            node_split_by_delimiter = node.text.split(delimiter)
            for i in range(len(node_split_by_delimiter)):
                if i % 2 == 0:
                    nodesoutput.append(TextNode(node_split_by_delimiter[i], text_type_text))
                else:
                    nodesoutput.append(TextNode(node_split_by_delimiter[i], texttype))

    return nodesoutput

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    nodesoutput = []
    for node in old_nodes:
        original_text = node.text
        image_list = extract_markdown_images(node.text)
        # if not image_list:
        #     print(node)
        #     nodesoutput.append(node)
        for image_tup in image_list:
            modified_text = original_text.split(f"![{image_tup[0]}]({image_tup[1]})")
            first_node = modified_text[0]

            nodesoutput.append(TextNode(first_node,text_type_text))
            nodesoutput.append(TextNode(image_tup[0],text_type_image,image_tup[1]))
            original_text = modified_text[1]
        nodesoutput.append(TextNode(original_text,text_type_text))
    return nodesoutput

def split_nodes_link(old_nodes):
    nodesoutput = []
    for node in old_nodes:
        original_text = node.text
        link_list = extract_markdown_links(node.text)
        # if not link_list:
        #     nodesoutput.append(node)
        for link_tup in link_list:
            modified_text = original_text.split(f"[{link_tup[0]}]({link_tup[1]})")
            first_node = modified_text[0]
            nodesoutput.append(TextNode(first_node,text_type_text))
            nodesoutput.append(TextNode(link_tup[0],text_type_image,link_tup[1]))
            original_text = modified_text[1]
        nodesoutput.append(TextNode(original_text,text_type_text))
    return nodesoutput


def apply_changes_to_textnodes(master_node_list, function_to_call, delimiter = None, text_type = None):
    changes = []
    #Step 2: Iterate on master list and collect changes in new list
    for i, node in enumerate(master_node_list):
        if node.text_type != text_type:
            if function_to_call == 'split_nodes_delimiter':
                split_list = split_nodes_delimiter([node], delimiter, text_type)
            elif function_to_call == 'split_nodes_image':
                split_list = split_nodes_image([node])
            elif function_to_call == 'split_nodes_link':
                split_list = split_nodes_link([node])
            if len(split_list) != 1:
                changes.append((i,split_list))
    
    #Step 3: Apply changes
    for index, new_nodes in reversed(changes):
        master_node_list[index:index+1] = new_nodes 

    return master_node_list

def text_to_textnodes(text):
    starting_node = TextNode(text,text_type_text)
    master_node_list = [starting_node]
    
    # Step 1: Populate master list with first (bold) treatment.
    master_node_list = split_nodes_delimiter(master_node_list, '**', text_type_bold)

    #Apply italic treatment    
    master_node_list = apply_changes_to_textnodes(master_node_list, 'split_nodes_delimiter', '*', text_type_italic)

    #Apply code treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, 'split_nodes_delimiter', '`', text_type_code)

    #Aply image treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, 'split_nodes_image')

    #Aply link treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, 'split_nodes_link')

    return master_node_list


def main():
    
    # node = TextNode(
    # "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some text after",
    # text_type_text,
    #     )
    # new_nodes = split_nodes_image([node])
    # print(new_nodes)

    # node = TextNode(
    # "Look at me i have no image",
    # text_type_text,
    #     )
    # new_nodes = split_nodes_image([node])
    # print(new_nodes)

    # node = TextNode(
    # "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
    # text_type_text,
    #     )
    # new_nodes = split_nodes_link([node])
    # print(new_nodes)


    text_to_parse = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    print(text_to_parse)
    test = text_to_textnodes(text_to_parse)
    print(test)


    




main()


