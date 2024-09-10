import html

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.attributes = self.props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        children_representation = self.children if self.children else None
        return f"HTMLNode({self.tag}, {self.value}, children: {children_representation}, {self.attributes})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == '':
            return html.escape(self.value)
        return f"<{self.tag}{self.props_to_html()}>{html.escape(self.value)}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children if children is not None else [], props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def append_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"