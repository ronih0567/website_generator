class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children #if children is not None else []
        self.props = props #if props is not None else {}

    def __to_html__(self):
        raise NotImplementedError
    
    def __props_to_html__(self, props):
        output_html = ""
        for entry in props.items():
            key, value = entry
            output_html += f' {key}="{value}"'
        
        return output_html
        #return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"