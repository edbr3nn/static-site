import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f, open(template_path) as t:
        markdown_content = f.read()
        template = t.read()
        html_string = markdown_to_html_node(markdown_content).to_html()
        full_html = template.replace("{{ Title }}", extract_title(markdown_content)).replace("{{ Content }}", html_string)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as w:
            w.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            if item_path.endswith(".md"):
                dest_file_path = os.path.join(dest_dir_path, Path(item).with_suffix(".html"))
                generate_page(item_path, template_path, dest_file_path)
        else:
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))
