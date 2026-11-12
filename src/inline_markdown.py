import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Delimiter not closed")
            for index, part in enumerate(parts):
                if part == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text) -> list:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text) -> list:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not extract_markdown_images(old_node.text):
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            remaining_text = old_node.text
            for image_alt, image_link in matches:
                sections = remaining_text.split(f"![{image_alt}]({image_link})")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not extract_markdown_links(old_node.text):
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            remaining_text = old_node.text
            for link_text, url in matches:
                sections = remaining_text.split(f"[{link_text}]({url})")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text) -> list:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
