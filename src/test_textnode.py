import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node3, node4)

    def test_uneq2(self):
        node5 = TextNode("This is a text node", TextType.LINK, "url.com")
        node6 = TextNode("This is a TEST node", TextType.LINK, "url.com")
        self.assertNotEqual(node5, node6)

    def test_text(self):
        node7 = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node7)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node8 = TextNode("bold text", TextType.BOLD)
        html_node8 = text_node_to_html_node(node8)

    def test_text_link(self):
        node9 = TextNode("duckduckgo", TextType.LINK, "www.duckduckgo.com")
        html_node9 = text_node_to_html_node(node9)
        self.assertEqual(html_node9.tag, "a")
        self.assertEqual(html_node9.value, "duckduckgo")
        self.assertEqual(html_node9.props, {"href": node9.url})

    def test_text_image(self):
        node10 = TextNode("stern serow", TextType.IMAGE, "sternserow.kom")
        html_node10 = text_node_to_html_node(node10)
        self.assertEqual(html_node10.tag, "img")
        self.assertEqual(html_node10.value, "")
        self.assertEqual(html_node10.props, {"src": node10.url, "alt": node10.text})

if __name__ == "__main__":
    unittest.main()
