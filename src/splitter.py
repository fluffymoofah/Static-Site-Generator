text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

from textnode import TextNode, text_node_to_html_node
import re
from htmlnode import LeafNode, ParentNode

def string_to_block(temp_block, block):
    if temp_block:
        block.append("\n".join(temp_block))

def markdown_to_blocks(markdown):
    temp_block = []
    block = []
    for string in markdown.splitlines():
        if len(string.strip()) != 0:
            temp_block.append(string.strip())
        else:
            string_to_block(temp_block, block)
            temp_block = []
    string_to_block(temp_block, block)
    return block

def block_to_block_type(block):
    if re.match(r'^#+\s', block):
        return block_type_heading
    if re.match(r'^```', block) and re.search(r'```$', block):
        return block_type_code
    if all(re.match(r'^>', line) for line in block.split('\n')):
        return block_type_quote
    if all(re.match(r'^[*-]', line) for line in block.split('\n')):
        return block_type_ulist
    if all(re.match(rf'^{index}\.', line) for index, line in enumerate(block.split('\n'), start=1)):
        return block_type_olist
    else:
        return block_type_paragraph
    
def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "text":
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiter")
            for index, part in enumerate(parts):
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, "text"))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
    
def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def create_heading_node(block):
    level = block.count('#', 0, block.find(' '))
    content = block[level:].strip()
    tag = f"h{min(level, 6)}"
    return LeafNode(tag, content)

def create_code_node(block):
    lines = block.split('\n')
    code_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else ""
    code_node = LeafNode('code', code_content)
    pre_node = ParentNode('pre', children=[code_node])
    return pre_node

def create_quote_node(block):
    quote_content = block[1:].lstrip()
    quote_node = ParentNode('blockquote', text_to_children(quote_content))
    return quote_node

def create_unordered_list_node(block):
    ul_node = ParentNode('ul', [])
    for item in block.splitlines():
        cleaned_item = item.lstrip('-*').strip()
        li_node = ParentNode('li', text_to_children(cleaned_item))
        ul_node.children.append(li_node)
    return ul_node

def create_ordered_list_node(block):
    ol_node = ParentNode('ol', [])
    for item in block.splitlines():
        cleaned_item = item.lstrip('0123456789.').strip()
        li_node = ParentNode('li', text_to_children(cleaned_item))
        ol_node.append_child(li_node)
    return ol_node

def create_paragraph_node(block):
    paragraph_content = block.strip()
    return ParentNode('p', children=text_to_children(paragraph_content))
    
def markdown_to_html_node(markdown):
    future_node = ParentNode('div', children=[])
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        if block_type == "heading":
            heading_node = create_heading_node(block)
            future_node.append_child(heading_node)

        elif block_type == "code":
            code_node = create_code_node(block)
            future_node.append_child(code_node)

        elif block_type == "quote":
            quote_node = create_quote_node(block)
            future_node.append_child(quote_node)

        elif block_type == "unordered_list":
            ulist_node = create_unordered_list_node(block)
            future_node.append_child(ulist_node)

        elif block_type == "ordered_list":
            olist_node = create_ordered_list_node(block)
            future_node.append_child(olist_node)

        else: 
            paragraph_node = create_paragraph_node(block)
            future_node.append_child(paragraph_node)
    return future_node
