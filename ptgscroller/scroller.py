"""
Classes used by the Scroller package.
"""

import pathlib
import tempfile
import tarfile
import xml.sax
from PIL import Image
from ptgscroller.xml_handler import MetaHandler, ContentHandler


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
        self.images = {}
        self.embed_size = 32

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

            for image_name in handler.images:
                image_path = list(tmpdir.glob(image_name))[0]

                image = Image.open(image_path)
                image = image.resize((self.embed_size, self.embed_size))
                self.images.update({image_name: image})


class Library:
    """
    Represents a directory that contains a collection of scroll files.

    When instantiated scans the directory indicated in the path attribute for scroll files and populates scroll's metadata attributes.

    Attributes:
        scrolls (dict): Scroll title key and scroll object value
        path (pathlib.Path): Path to library directory
    """

    def __init__(self, path: pathlib.Path = "./scroll_library") -> None:
        self.scrolls = {}
        self.path = pathlib.Path(path)

        self.scan()

    def find(self, title: str) -> Scroll:
        """
        Get a scroll object from a library.

        Args:
            title (str): A scroll's title
        Returns:
            The corresponding scroll object matching the given title
        """
        return self.scrolls.get(title)

    def scan(self) -> None:
        """
        Look through library directory and populate for found scroll files. Fill in scroll file's metadata.
        """
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
