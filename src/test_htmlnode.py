import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="Hello, world!", children=[], props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank",})
    
    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="Hello, world!", children=[], props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.__props_to_html__(node.props), ' href="https://www.google.com" target="_blank"')
        
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello, world!", children=[], props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, world!, [], {'href': 'https://www.google.com', 'target': '_blank'})")
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.__to_html__(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.__to_html__(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Italic text!")
        self.assertEqual(node.__to_html__(), "<i>Italic text!</i>")
        
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text!")
        self.assertEqual(node.__to_html__(), "<b>Bold text!</b>")
        
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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()