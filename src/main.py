from textnode import *
from htmlnode import *
import re

#define possible text types
text_types = ["text", "bold", "italic", "code", "link", "image"]
text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image = "text", "bold", "italic", "code", "link", "image"

#define possible block types
block_type_paragraph, block_type_heading, block_type_code = "paragraph", "heading", "code"
block_type_quote, block_type_unordered_list, block_type_ordered_list = "quote", "unordered_list", "ordered_list"

def escape_special_characters(text):
    # Replace '\*' and '\`' with a placeholder
    text = text.replace("\\*", "ESCAPED_ASTERISK").replace("\\`", "ESCAPED_BACKTICK")
    return text

def unescape_special_characters(text):
    # Replace the placeholder to literal '*' in final output
    text = text.replace("ESCAPED_ASTERISK", "*").replace("ESCAPED_BACKTICK", "`")
    return text

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
                    nodesoutput.append(TextNode(unescape_special_characters(node_split_by_delimiter[i]), text_type_text))
                else:
                    nodesoutput.append(TextNode(unescape_special_characters(node_split_by_delimiter[i]), texttype))

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
        for image_tup in image_list:
            modified_text = original_text.split(f"![{image_tup[0]}]({image_tup[1]})")
            first_node = modified_text[0]

            nodesoutput.append(TextNode(unescape_special_characters(first_node),text_type_text))
            nodesoutput.append(TextNode(unescape_special_characters(image_tup[0]),text_type_image,image_tup[1]))
            original_text = modified_text[1]
        nodesoutput.append(TextNode(unescape_special_characters(original_text),text_type_text))
    return nodesoutput

def split_nodes_link(old_nodes):
    nodesoutput = []
    for node in old_nodes:
        original_text = node.text
        link_list = extract_markdown_links(node.text)
        for link_tup in link_list:
            modified_text = original_text.split(f"[{link_tup[0]}]({link_tup[1]})")
            first_node = modified_text[0]
            nodesoutput.append(TextNode(unescape_special_characters(first_node),text_type_text))
            nodesoutput.append(TextNode(unescape_special_characters(link_tup[0]),text_type_image,link_tup[1]))
            original_text = modified_text[1]
        nodesoutput.append(TextNode(unescape_special_characters(original_text),text_type_text))
    return nodesoutput


def apply_changes_to_textnodes(master_node_list, processing_function, delimiter = None, text_type = None):
    changes = []
    #Step 2: Iterate on master list and collect changes in new list
    for i, node in enumerate(master_node_list):
        if node.text_type != text_type:
            if delimiter is not None:
                split_list = processing_function([node], delimiter, text_type)
            else:
                split_list = processing_function([node])
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
    master_node_list = apply_changes_to_textnodes(master_node_list, split_nodes_delimiter, '*', text_type_italic)

    #Apply code treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, split_nodes_delimiter, '`', text_type_code)

    #Aply image treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, split_nodes_image)

    #Aply link treatment
    master_node_list = apply_changes_to_textnodes(master_node_list, split_nodes_link)

    return master_node_list


def markdown_to_blocks(markdown):
    markdown_list = [block for block in markdown.split('\n\n')]
    for i,value in enumerate(markdown_list):
        markdown_list[i] = value.strip()
    return markdown_list

def block_to_block_type(block_text):
    if re.findall(r"^#{1,6} ",block_text):
        return block_type_heading
    if re.findall(r"^```.*\n*```$",block_text):
        return block_type_code
    if len(re.findall(r"^> ",block_text, re.MULTILINE)) == block_text.count('\n') + 1:
        return block_type_quote
    if len(re.findall(r"^[*-] ",block_text, re.MULTILINE)) == block_text.count('\n') + 1:
        return block_type_unordered_list
    #TODO: NEED TO CHECK FOR ORDERED LIST PATTERN

    return block_type_paragraph 
    

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


    # text_to_parse = "This is **text** with an *italic* word and a `code block` **and a rude word ** ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)[link](https://boot.dev)"
    # treated_text_to_parse =escape_special_characters(text_to_parse)
    # print(text_to_parse)
    # print('\n')
    # print(treated_text_to_parse)
    # test = text_to_textnodes(treated_text_to_parse)
    # print(test)

#     markdown_document ="""     This is **bolded** paragraph     

# This is another paragraph with *italic* text and `code` here
# This is the same paragraph on a new line


     
# * This is a list      
# * with items
# """
#     print(markdown_document)
#     print(markdown_to_blocks(markdown_document))


    block_text = """> This is an unordered list!
> This is a continuation!
> This is another continuation!
> blabalba"""
    print(block_to_block_type(block_text))
    


    




main()


