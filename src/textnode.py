text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    valid_types = {
        "text",
        "bold",
        "italic",
        "code",
        "link",
        "image"
    }
    if text_node.text_type not in valid_types:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode(tag='b', value=text_node.text.strip('*'))
    if text_node.text_type == "italic":
        return LeafNode(tag='i', value=text_node.text.strip('*'))
    if text_node.text_type == "code":
        return LeafNode(tag='code', value=text_node.text.strip('`'))
    if text_node.text_type == "link":
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
    if text_node.text_type == "image":
        return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})