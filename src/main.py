from textnode import TextNode
from htmlnode import HTMLNode



def main():
    
    test1 = HTMLNode('a', 'texto de teste', None, {"href": "https://www.google.com", "target": "_blank"})

    print(test1.__repr__())

main()
