class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __eq__(self, other: object) -> bool:
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

    def __repr__(self):
        return(
            f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None , value: str, props: dict | None = None):
        super(LeafNode, self).__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag == None:
            return(self.value)

        return(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")

    def __repr__(self):
        return(
            f"LeafNode({self.tag}, {self.value}, {self.props})"
        )

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super(ParentNode, self).__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")

        if not self.children:
            raise ValueError("All parent nodes must have children")

        children_html = ""
        for item in self.children:
            children_html += item.to_html()

        return(f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>")

    def __repr__(self):
        return(
            f"ParentNode({self.tag}, {self.children}, {self.props})"
        )
