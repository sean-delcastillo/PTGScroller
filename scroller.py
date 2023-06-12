import pathlib
import tempfile
import tarfile
import xml.sax
from xml_readers import MetaHandler, ContentHandler


class Scroll:
    """
    Represents a scroll (*.scrl) file.

    The Scroll class provides functionality to read and navigate through the contents of a scroll file.

    Attributes:
        path (pathlib.Path): The path to the scroll file
        title (str): The title of the scroll
        meta (dict): A dictionary of meta attributes of a scroll ("Author", "Publish Date", etc)
        content (dict): The textual contents of the scroll file keyed by section number
    """

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.title = ""
        self.meta = {}
        self.content = {}

    def open(self):
        """
        Extracts the scroll file archive, parses the content.xml file, and inserts text content into content attribute.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            with tarfile.open(self.path) as tar:
                tar.extractall(tmpdir)

            tmpdir = pathlib.Path(tmpdir)
            content_file = list(tmpdir.glob("content.xml"))[0]

            handler = ContentHandler()
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(content_file)

            self.content = handler.scroll_attributes.get("sections")


class Library:
    def __init__(self, path: pathlib.Path = "./scroll_library") -> None:
        self.scrolls = {}
        self.path = pathlib.Path(path)

        self.scan()

    def find(self, title: str) -> Scroll:
        return self.scrolls.get(title)

    def scan(self) -> None:
        for scroll_tar in self.path.glob("*.scrl"):
            with tempfile.TemporaryDirectory() as tmpdir:
                with tarfile.open(scroll_tar) as tar:
                    tar.extractall(tmpdir)

                tmpdir = pathlib.Path(tmpdir)
                content_file = list(tmpdir.glob("content.xml"))[0]

                handler = MetaHandler()
                parser = xml.sax.make_parser()
                parser.setContentHandler(handler)
                parser.parse(content_file)

                scroll = Scroll(scroll_tar)
                scroll.title = handler.get("title")
                scroll.meta = handler.meta_data

                self.scrolls.update({scroll.title: scroll})
