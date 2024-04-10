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
    def __init__(self, value, tag = None, props = None):
        if value is None:
            raise ValueError('All leaf nodes require a value!')
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


