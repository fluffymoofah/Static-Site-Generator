from splitter import text_to_textnodes, text_to_children
from textnode import text_node_to_html_node

def test_text_to_children():
    input_text = "This is **bold** and *italic* text with `code`."
    result = text_to_children(input_text)
    
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