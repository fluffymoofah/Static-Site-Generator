from splitter import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]