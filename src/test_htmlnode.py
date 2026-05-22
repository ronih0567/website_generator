import unittest
from htmlnode import HTMLNode

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