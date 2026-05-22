class TextNode:
    def __init__(self, text, type, url=None):
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            getattr(self, "text", None) == getattr(other, "text", None)
            and getattr(self, "text_type", None) == getattr(other, "text_type", None)
            and getattr(self, "url", None) == getattr(other, "url", None)
        )

    def __repr__(self):
        text = "" if self.text is None else str(self.text)
        text_type = "" if self.text_type is None else str(self.text_type)
        url = "" if self.url is None else str(self.url)
        return f"TextNode({text}, {text_type}, {url})"