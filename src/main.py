from textnode import TextNode


def main():
    
    test1 = TextNode('teste texto', 'pdf', "https://www.youtube.com")
    test2 = TextNode('teste texto', 'pdf', "https://www.youtube.com")

    print(test1.__repr__())
    print(test2.__repr__())



main()
