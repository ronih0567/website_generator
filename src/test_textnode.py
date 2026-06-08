import unittest
from src.main import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    text_node_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
)
from textnode import TextNode, TextType, BlockType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
        
    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)
    
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        
    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is a image node"})

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_ignores_links(self):
        text = "This has [a link](https://example.com) and ![an image](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("an image", "https://example.com/image.png")],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "This has [a link](https://example.com) and ![an image](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_links(text),
            [("a link", "https://example.com")],
        )

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_preserves_non_text_nodes(self):
        old_nodes = [
            TextNode("Start **bold**", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_raises_on_unmatched_delimiter(self):
        node = TextNode("This has `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_nodes_link_ignores_images(self):
        node = TextNode(
            "Text [a link](https://example.com) and ![an image](https://example.com/image.png)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(" and ![an image](https://example.com/image.png)", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_preserves_non_text_nodes(self):
        old_nodes = [
            TextNode("![an image](https://example.com/image.png)", TextType.TEXT),
            TextNode("already a link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(
            split_nodes_image(old_nodes),
            [
                TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode("already a link", TextType.LINK, "https://example.com"),
            ],
        )
        
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )

    def test_text_to_textnodes_plain_text(self):
        self.assertEqual(
            text_to_textnodes("This is plain text"),
            [TextNode("This is plain text", TextType.TEXT)],
        )

    def test_text_to_textnodes_bold(self):
        self.assertEqual(
            text_to_textnodes("This has **bold** text"),
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_bold_and_italic(self):
        self.assertEqual(
            text_to_textnodes("This has **bold** and _italic_ text"),
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_code_and_link(self):
        self.assertEqual(
            text_to_textnodes("Run `python3 main.py` then visit [Boot.dev](https://www.boot.dev)"),
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("python3 main.py", TextType.CODE),
                TextNode(" then visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_text_to_textnodes_image_and_link(self):
        self.assertEqual(
            text_to_textnodes("See ![logo](https://example.com/logo.png) and [site](https://example.com)"),
            [
                TextNode("See ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
        )

    def test_text_to_textnodes_all_types(self):
        self.assertEqual(
            text_to_textnodes("A **bold** _italic_ `code` ![img](https://example.com/img.png) [link](https://example.com)"),
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test1_markdown_to_blocks(self):
        md = """This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        # print(f"blocks: {blocks}")
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test2_markdown_to_blocks(self):
        md = """This is an _italicized_ paragraph

This is another paragraph with `code` here and **bold text** here
This is the same paragraph on a new line
This is the same paragraph on yet another new line

- This is a list
- Peas porrige hot
- Peas porrige cold
- Peas porrige in the pot
- Nine days old"""
        blocks = markdown_to_blocks(md)
        #print(f"blocks: {blocks}")
        self.assertEqual(
            blocks,
            [
                "This is an _italicized_ paragraph",
                "This is another paragraph with `code` here and **bold text** here\nThis is the same paragraph on a new line\nThis is the same paragraph on yet another new line",
                "- This is a list\n- Peas porrige hot\n- Peas porrige cold\n- Peas porrige in the pot\n- Nine days old",
            ],
        )
        
    def test3_markdown_to_blocks(self):
        md = """The next block should be removed due to being empty




This is another paragraph with `code` here, **bold text** here
and _italic text_ here

- Another list
- Spam
- Spam spam eggs and spam
- Spam spam spam eggs and spam"""
        blocks = markdown_to_blocks(md)
        #print(f"blocks: {blocks}")
        self.assertEqual(
            blocks,
            [
                "The next block should be removed due to being empty",
                "This is another paragraph with `code` here, **bold text** here\nand _italic text_ here",
                "- Another list\n- Spam\n- Spam spam eggs and spam\n- Spam spam spam eggs and spam",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        

if __name__ == "__main__":
    unittest.main()
