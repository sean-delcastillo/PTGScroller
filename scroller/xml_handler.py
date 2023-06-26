"""
Sax content handlers used to parse scroll files (*.scrl).

MetaHandler is used by the Library to fill in the scroll's meta data attributes,
while the ContentHandler is used by the Scroll to fill in its contents.
"""

import xml.sax


class MetaHandler(xml.sax.ContentHandler):
    def __init__(self) -> None:
        self.meta_data = {}

    def get(self, key: any) -> any:
        return self.meta_data.get(key)

    def startElement(self, name, attrs):
        if name == "META":
            self.meta_data.update(attrs.items())


class ContentHandler(xml.sax.ContentHandler):
    def __init__(self) -> None:
        self.scroll_attributes = {}
        self._current_data = ""
        self.sections = {}
        self._section_content = []
        self.images = []
        self._paragraph_content = ""
        self.section_count = 0

    def startElement(self, tag, attributes):
        self._current_data = tag
        match self._current_data:
            case "section":
                self.section_count += 1
            case "img":
                self._section_content.append(f"IMGFILE:{attributes.get('src')}")
                self.images.append(f"{attributes.get('src')}")

    def endElement(self, tag):
        match tag:
            case "paragraph":
                self._paragraph_content += "\n\n"
                self._section_content.append(self._paragraph_content)
                self._paragraph_content = ""
            case "section":
                self.sections.update({self.section_count: self._section_content})
                self._section_content = []

    def characters(self, content):
        match self._current_data:
            case "paragraph":
                content = content.strip()
                if content.isprintable():
                    content_parts = content.rpartition("\n")
                    if content_parts[1] != "":
                        content = content_parts[0] + content_parts[2]
                    self._paragraph_content += content

    def endDocument(self):
        self.scroll_attributes.update({"sections": self.sections})
