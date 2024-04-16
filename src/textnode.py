import re
from htmlnode import *

#define possible text types
text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image = "text", "bold", "italic", "code", "link", "image"

#define possible block types
block_type_paragraph, block_type_heading, block_type_code = "paragraph", "heading", "code"
block_type_quote, block_type_unordered_list, block_type_ordered_list = "quote", "unordered_list", "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def __eq__(self,node):
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
    
def escape_special_characters(text):
    # Replace '\*' and '\`' with a placeholder
    text = text.replace("\\*", "ESCAPED_ASTERISK").replace("\\`", "ESCAPED_BACKTICK")
    return text

def unescape_special_characters(text):
    # Replace the placeholder to literal '*' in final output
    text = text.replace("ESCAPED_ASTERISK", "*").replace("ESCAPED_BACKTICK", "`")
    return text

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
                if i % 2 == 0 and node_split_by_delimiter[i] != '':
                    nodesoutput.append(TextNode(unescape_special_characters(node_split_by_delimiter[i]), text_type_text))
                elif node_split_by_delimiter[i] != '':
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
    # text_split = text.split('\n')
    # master_node_list = []
    # for value in text_split:
    #     master_node_list.append(TextNode(value,text_type_text))    
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
    if len(re.findall(r"^\d+\. ",block_text, re.MULTILINE)) == block_text.count('\n') + 1:
        block_text_list = block_text.split('\n')
        for i in range(len(block_text_list)):
            number_to_check = i + 1
            number_in_list = block_text_list[i].split('.')[0]
            if str(number_to_check) != number_in_list:
                return block_type_paragraph
        return block_type_ordered_list
    return block_type_paragraph

def from_mdBlock_to_HTMLNode(md_block, block_type):
    html_nodes = []
    
    if isinstance(md_block, str):
        md_block = [md_block]
    
    if block_type == block_type_paragraph:
        leaf_node = LeafNode(None, md_block[0], None)
        html_nodes.append(ParentNode("p", None, [leaf_node], None))
    
    elif block_type == block_type_quote:
        leaf_node = LeafNode(None, md_block[0][1:].strip(), None)
        html_nodes.append(ParentNode("blockquote", None, [leaf_node], None))

    elif block_type == block_type_unordered_list:
        li_wrapped = []
        for block in md_block:
            lines = block.split('\n')
            for line in lines:
                new_line = line[1:].strip()
                li_wrapped.append(LeafNode("li", new_line))
        html_nodes.append(ParentNode("ul", None, li_wrapped))

    elif block_type == block_type_ordered_list:
        li_wrapped = []
        for block in md_block:
            lines = block.split('\n')
            for line in lines:
                if '.' in line:
                    new_line = line[line.index('.') + 1:].strip()
                    li_wrapped.append(LeafNode("li", new_line))
        html_nodes.append(ParentNode("ol",None, li_wrapped))

    elif block_type == block_type_code:
        for block in md_block:
            new_block = block.strip("```")
            pre_covered = LeafNode("pre", new_block)
            html_nodes.append(ParentNode("code", None, [pre_covered]))
    
    elif block_type == block_type_heading:
        heading_prefixes = {
            "# ": "h1",
            "## ": "h2",
            "### ": "h3",
            "#### ": "h4",
            "##### ": "h5",
            "###### ": "h6"
        }
        for prefix, tag in heading_prefixes.items():
            for block in md_block:
                if block.startswith(prefix):
                    block = block[len(prefix):]
                    leaf_node = LeafNode(None, block, None)
                    html_nodes.append(ParentNode(tag, None, [leaf_node], None))

    return html_nodes

def markdown_to_html_node(markdown):
    children = []
    block_list = markdown_to_blocks(markdown)
    inline_leaf_nodes = []
    leaf_nodes_to_html = ""
    for block in block_list:
        block_escaped = escape_special_characters(block)
        text_nodes = text_to_textnodes(block_escaped)
        inline_leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        leaf_nodes_to_html += ''.join(leaf_node.to_html() for leaf_node in inline_leaf_nodes) +"\n\n"
    new_blocks = markdown_to_blocks(leaf_nodes_to_html)
    for new_block in new_blocks:
        block_type = block_to_block_type(new_block)
        children.extend(from_mdBlock_to_HTMLNode(new_block, block_type))
    return ParentNode("div", None,children).to_html()