import unittest
from markdown_blocks import *

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        block_zero = "This is plain paragraph text."
        block_one = "# This block is a heading."
        block_two = "```\nThis block is two lines\nof code.```"
        block_three = "> This block is \n>quoted text \n>oh yes"
        block_four = "- This is an unordered list\n- This is the second line"
        block_five = "1. This is an ordered list\n2. This is the second line\n3. This is the third"

        self.assertEqual(block_to_block_type(block_zero), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_one), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block_two), BlockType.CODE)
        self.assertEqual(block_to_block_type(block_three), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block_four), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block_five), BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        print(repr(md))
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
