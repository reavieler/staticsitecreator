from textnode import *
from htmlnode import *
import re
import os
import shutil

def extract_title(markdown):
    markdown_lines = markdown.split('\n')
    if markdown_lines[0].startswith('# ') == False:
        raise Exception('All pages need a single h1 header.')
    return markdown_lines[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path) as markdown_file:
        markdown_content = markdown_file.read()
    with open(template_path) as template_file:
        template_html = template_file.read()
    page_title = extract_title(markdown_content)
    html_content = markdown_to_html_node(markdown_content)
    final_html = template_html.replace('{{ Title }}',page_title).replace('{{ Content }}',html_content)
    with open(dest_path, "w") as html_dest:
        html_dest.write(final_html)
    print("All done!")
    return

def clear_public_folder(folder_path):
    if not os.path.isdir(folder_path):
        return
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            print(f"Removing {item_path}...")
            os.remove(item_path)
        elif os.path.isdir(item_path):
            clear_public_folder(item_path)
    if folder_path != 'public':
        print(f"Removing {folder_path}...")
        os.rmdir(folder_path)
            
def copy_directory_contents(source, destination):
    if not os.path.isdir(destination):
        print(f"Destination does not exist! Creating {destination}...")
        os.mkdir(destination)
    for item in os.listdir(source):
        item_source = os.path.join(source, item)
        item_destination = os.path.join(destination, item)
        if os.path.isdir(item_source):
            print(f"Creating {item_destination}...")
            os.mkdir(item_destination)
            copy_directory_contents(item_source, item_destination)
        else:
            print(f"Creating {item_destination}...")
            shutil.copy(item_source, item_destination)




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


    clear_public_folder("public")
    copy_directory_contents("static", "public")
    generate_page("content/index.md","template.html","public/index.html")
    




main()


