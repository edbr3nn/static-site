import unittest
from textnode import TextNode, TextType
from inline_markdown import *

class TestInLineMarkdown(unittest.TestCase):
    def test_inline_markdown(self):
        node = TextNode("This is a **bold** test", TextType.TEXT)
        print(split_nodes_delimiter([node], "**", TextType.BOLD))

        node_two = TextNode("This is an _italic_ test", TextType.TEXT)
        print(split_nodes_delimiter([node_two], "_", TextType.ITALIC))

        node_three = TextNode("`code code code` this is a `code` block test", TextType.TEXT)
        print(split_nodes_delimiter([node_three], "`", TextType.CODE))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Here is a [link](https://verdantanglepress.com)"
        )
        self.assertListEqual([("link", "https://verdantanglepress.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_full_output(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        full_output = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            full_output,
        )

        bold_node = "**this is bold text only**"
        bold_output = text_to_textnodes(bold_node)
        self.assertListEqual(
            [
                TextNode("this is bold text only", TextType.BOLD)
            ],
            bold_output,
        )


        plain_node = "this is plain text"
        plain_output = text_to_textnodes(plain_node)
        self.assertListEqual(
            [
                TextNode("this is plain text", TextType.TEXT)
            ],
            plain_output,
        )
