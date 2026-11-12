import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_children = ["child1", "child2", "child3"]
        test_dictionary = {"href": "one", "target": "two"}
        node = HTMLNode("tag", "value", test_children, test_dictionary)
        node2 = HTMLNode("tag", "value", test_children, test_dictionary)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node3 = HTMLNode()
        node4 = HTMLNode("taggyMcTaggins")
        self.assertNotEqual(node3, node4)

    def test_uneq2(self):
        node5 = HTMLNode("tag", "lalala", ["item1", "item2"])
        node6 = HTMLNode()
        self.assertNotEqual(node5, node6)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_href(self):
        node = LeafNode("a", "Click this link", {"href": "https://www.duckduckgo.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.duckduckgo.com">Click this link</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, "blue")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
