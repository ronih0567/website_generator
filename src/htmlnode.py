class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __to_html__(self):
        raise NotImplementedError
    
    def __props_to_html__(self, props):
        output_html = ""
        for entry in props.items():
            key, value = entry
            output_html += f' {key}="{value}"'
        
        return output_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)
        
    def __to_html__(self):
        if self.value is None:
            return ValueError("Leaf nodes must have a value")
        elif self.tag is None:
            return str(self.value)
        else:
            props_html = self.__props_to_html__(self.props) if self.props else ""
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props=None)
        
    def __to_html__(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("Parent nodes must have children")
        else:
            props_html = self.__props_to_html__(self.props) if self.props else ""
            children_html = "".join([child.__to_html__() for child in self.children])
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
            
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"