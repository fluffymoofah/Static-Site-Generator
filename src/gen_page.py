import os
from splitter import markdown_to_html_node

def extract_title(markdown):
    for string in markdown.splitlines():
        if string.startswith('# '):
            return string[2:].strip()
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}, please stand by.")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if directory != "":
        os.makedirs(directory, exist_ok=True)
    
    with open(dest_path, 'w') as file:
        file.write(template)