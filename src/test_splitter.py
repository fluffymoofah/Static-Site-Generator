import unittest
from textnode import TextNode
import splitter

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_string(self):
        markdown = " This is a string of text. There are no empty lines in this string of text."
        expected = ["This is a string of text. There are no empty lines in this string of text."]
        result = splitter.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_multi_string(self):
        markdown = """This is a string of text.

This is also a string of text. """
        expected = ["This is a string of text.", "This is also a string of text."]
        result = splitter.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_no_string(self):
        markdown = ""
        expected = []
        result = splitter.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_quote)
        block = "* list\n* items"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_olist)
        block = "paragraph"
        self.assertEqual(splitter.block_to_block_type(block), splitter.block_type_paragraph)

    def test_paragraph_node(self):
        markdown = "This is a paragraph."
        node = splitter.markdown_to_html_node(markdown)
        paragraph_node = node.children[0]
        self.assertEqual(paragraph_node.tag, "p")
        self.assertEqual(paragraph_node.value, "This is a paragraph.")

    def test_heading_node(self):
        markdown = "# Heading"
        node = splitter.markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        heading_node = node.children[0]
        self.assertEqual(heading_node.tag, "h1")
        self.assertEqual(heading_node.value, "Heading")

    def test_code_node(self):
        markdown = "```\ncode\n```"
        node = splitter.markdown_to_html_node(markdown)
        pre_node = node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.value, "code")

    def test_quote_node(self):
        markdown = "> This is a quote."
        node = splitter.markdown_to_html_node(markdown)
        quote_node = node.children[0]
        self.assertEqual(quote_node.tag, "blockquote")
        self.assertEqual(quote_node.value, "This is a quote.")

    def test_unordered_list_node(self):
        markdown = "- Item 1\n- Item 2"
        node = splitter.markdown_to_html_node(markdown)
        ulist_node = node.children[0]
        self.assertEqual(ulist_node.tag, "ul")
        self.assertEqual(ulist_node.children[0].tag, "li")
        self.assertEqual(ulist_node.children[0].value, "Item 1")
        self.assertEqual(ulist_node.children[1].tag, "li")
        self.assertEqual(ulist_node.children[1].value, "Item 2")

    def test_ordered_list_node(self):
        markdown = "1. First item\n2. Second item"
        node = splitter.markdown_to_html_node(markdown)
        olist_node = node.children[0]
        self.assertEqual(olist_node.tag, "ol")
        self.assertEqual(olist_node.children[0].tag, "li")
        self.assertEqual(olist_node.children[0].value, "First item")
        self.assertEqual(olist_node.children[1].tag, "li")
        self.assertEqual(olist_node.children[1].value, "Second item")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is 'code' in text.", text_type_text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" in text.", text_type_text)
        ]
        result = splitter.split_nodes_delimiter([node], "'", text_type_code)
        self.assertEqual(result, expected)
    
    def test_unmatched_delimiter(self):
        node = TextNode("This has an unmatched * delimiter", text_type_text)
        with self.assertRaises(Exception):
            splitter.split_nodes_delimiter([node], "*", text_type_italic)
    
    def test_no_delimiter(self):
        node = TextNode("Just plain text without delimiters", text_type_text)
        expected = [node]
        result = splitter.split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(result, expected)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        result = splitter.extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        result = splitter.extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_neither(self):
        text = "This is a text with neither."
        expected = []
        result_images = splitter.extract_markdown_images(text)
        result_links = splitter.extract_markdown_links(text)
        self.assertEqual(result_images, expected)
        self.assertEqual(result_links, expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = splitter.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = splitter.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = splitter.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = splitter.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = splitter.text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )

def test_text_to_children():
    input_text = "This is **bold** and *italic* text with `code`."
    result = splitter.text_to_children(input_text)
    
    # Print the result for inspection
    print("Resulting HTML nodes:")
    for node in result:
        print(node.to_html())
    
    # You can also add assertions here to automatically check the output
    # For example:
    # assert result[1].to_html() == "<b>bold</b>"
    # assert result[3].to_html() == "<i>italic</i>"
    # assert result[7].to_html() == "<code>code</code>"

# Run the test
test_text_to_children()

if __name__ == "__main__":
    unittest.main()