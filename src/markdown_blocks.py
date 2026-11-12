from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            new_blocks.append(stripped_block)

    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    parts = block.split(" ", 1)
    first_chunk = parts[0]
    if 0 < len(first_chunk) <= 6 and first_chunk.count("#") == len(first_chunk) and len(parts) > 1:
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(block.split("\n"))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown) -> HTMLNode:
    new_nodes = []
    li_children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_lines = block.split("\n")
            clean_paragraph_lines = []
            for line in paragraph_lines:
                clean_paragraph_lines.append(line.strip())
            children = text_to_children(" ".join(clean_paragraph_lines))
            new_nodes.append(ParentNode("p", children))

        elif block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char != "#":
                    break
                elif char == "#":
                    count += 1
            trimmed_block = block[count:].strip()
            children = text_to_children(trimmed_block.replace("\n", " "))
            new_nodes.append(ParentNode(f"h{count}", children))

        elif block_type == BlockType.CODE:
            code_lines = block.split("\n")
            clean_code_lines = []
            for line in code_lines:
                clean_code_lines.append(line.strip())
            code_block = text_node_to_html_node(TextNode("\n".join(clean_code_lines[1:-1])+ "\n", TextType.TEXT))
            new_nodes.append(ParentNode("pre", [ParentNode("code", [code_block])]))

        elif block_type == BlockType.QUOTE:
            quote_lines = block.split("\n")
            clean_quote_lines = []
            for line in quote_lines:
                clean_quote_lines.append(line[1:].strip())
            quote_string = " ".join(clean_quote_lines)
            children = text_to_children(quote_string)
            new_nodes.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            list_lines = block.split("\n")
            li_children = []
            for line in list_lines:
                li_children.append(ParentNode("li", text_to_children(line[2:])))
            new_nodes.append(ParentNode("ul", li_children))

        elif block_type == BlockType.ORDERED_LIST:
            list_lines = block.split("\n")
            li_children = []
            for line in list_lines:
                count = 0
                for char in line:
                    if char == " ":
                        line_count = count
                        break
                    else:
                        count += 1
                li_children.append(ParentNode("li", text_to_children(line[count:].strip())))
            new_nodes.append(ParentNode("ol", li_children))

    return ParentNode("div", new_nodes)

def text_to_children(text) -> list:
    html_nodes = []

    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
