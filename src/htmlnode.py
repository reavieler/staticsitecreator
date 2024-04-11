class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def props_to_html(self):
        output = ''
        for key in self.props:
            output += f' {key}="{self.props[key]}"'
        return output
    
    def to_html(self):
        raise NotImplementedError("That task has not been completed!")


class LeafNode(HTMLNode):
    def __init__(self, tag = None,value = None, children = None, props = None):
        if value is None:
            raise ValueError('All leaf nodes require a value!')
        if children is not None:
            raise ValueError('Leaf nodes can\'t contain children!')
        super().__init__(tag, value, children, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        elif self.props is not None:
            props_value = self.props_to_html()
            return f"<{self.tag}{props_value}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag = None,value = None, children = None, props = None):
        if value is not None:
            raise ValueError('No Parent nodes can have a value!')
        if children is None or children == []:
            raise ValueError('Parent nodes must have children!')
        if tag is None:
            raise ValueError('Need to provide tag to parent node!')
        super().__init__(tag, value, children, props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        output = ""
        for child in self.children:
            output += child.to_html()
        return f"<{self.tag}>{output}</{self.tag}>"

        



