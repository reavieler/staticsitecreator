from textnode import *
from htmlnode import *
import re
import os
import shutil

def copy_static():
    paths = []
    test = os.listdir('static')
    print(test)





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

#     markdown ="""This is a **bolded** paragraph     

# This is another paragraph with *italic* text and `code` here
# This is the same paragraph on a new line

# ```This is a block of code and this is a block of code still```

# - This is a list
# - This is still a list"""
#     #markdown = """```This is a block of code and this is a block of code still```"""
#     # print(markdown)
#     # print(markdown_to_html_node(markdown))
#     print(markdown_to_html_node(markdown))
    # block_list = markdown_to_blocks(markdown_document)
    # for block in block_list:

    #     block_type = block_to_block_type(block)
    #     if block_type == block_type_heading:
    #         heading_leaf_node = heading_to_html_node(block)
    #         print(heading_leaf_node)

    copy_static()
    




main()


