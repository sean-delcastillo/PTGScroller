"""
Importable Scroller widgets.
"""

from typing import Any
import pytermgui as ptg
import pathlib
from ptgscroller.scroller import Library
from PIL import Image


class ScrollLibrary(ptg.Container):
    """
    A widget that generates a button for each scroll file in the library directory.

    Attributes:
        library (Library): Library instance to build the buttons from
        library_name (str): The name of the library instance
        window_manager (ptg.WindowManager): The PyTermGui windowmanager
    """

    def __init__(
        self,
        window_manager: ptg.WindowManager,
        library_dir: pathlib.Path = "./scroll_library",
        **attrs: Any,
    ) -> None:
        super().__init__(**attrs)
        attrs.update({"box": "EMPTY"})

        self.reader_embed_size = attrs.get("embed_size")
        if self.reader_embed_size is None:
            self.reader_embed_size = 32

        self.library = Library(library_dir)
        self.library_name = self.library.path.name
        self.window_manager = window_manager

        self.update_content()

    def _button_handler(self, scroll_title: str) -> callable:
        """
        Creates a function that creates a ScrollReader instance of the given scroll title.

        Args:
            scroll_title (str): The title of the scroll to open

        Returns:
            A function that opens a window with a ScrollReader of the given scroll
        """
        title = scroll_title

        def set_default_width() -> int:
            if self.reader_embed_size < 100:
                return 100
            else:
                return self.reader_embed_size + 50

        def draw_scroll_window(*_):
            reader = ScrollReader(self.library, title, self.reader_embed_size)
            exit = ptg.Button("X", lambda *_: window.close())

            window = (
                ptg.Window(exit, reader, width=set_default_width())
                .center()
                .set_title(reader.scroll_title)
            )

            self.window_manager.add(window)

        return draw_scroll_window

    def _generate_library_buttons(self) -> list[ptg.Button]:
        """
        Creates a list of PyTermGUI buttons for each scroll in a library directory that opens the corresponding scroll when clicked.

        Returns:
            A list of PyTermGUI buttons in PyTermGUI's auto syntax
        """
        library_buttons = []
        for title, scroll in self.library.scrolls.items():
            button = ptg.Button(title, self._button_handler(title))
            library_buttons.append(button)

        return library_buttons

    def update_content(self) -> None:
        """
        Create a container that contains generated library buttons and sets the ScrollLibrary's widgets.
        """
        buttons = ptg.Container(*self._generate_library_buttons(), box="EMPTY")

        self.set_widgets([buttons])


class ScrollReader(ptg.Container):
    """
    A widget that displays the content of a scroll file in a scrollable widget.

    Attributes:
        library (Library): Library instance to search through
        scroll_title (str): The title of the scroll to search for
        **attrs (Any): Attributes to pass to the widget
    """

    def __init__(
        self,
        library: Library,
        scroll_title: str,
        embed_size: int = 32,
        **attrs: Any,
    ) -> None:
        """
        Finds the corresponding scroll object using the scroll_title in the given library object, opens the scroll, and updates the widget's contents.
        """
        super().__init__(**attrs)
        attrs.update({"box": "EMPTY"})
        self.scroll_title = scroll_title
        self._scroll = library.find(scroll_title)

        self._scroll.embed_size = embed_size
        self._scroll.open()

        self.current_page = 1
        self.scroll_length = len(self._scroll.content.keys())

        self._inject_images()

        self._update_content()

    def _build_embed_image(self, image: Image):
        """
        Build a DensePixelMatrix from an Image object by setting matrix values according to the corresponding pixel value.

        Args:
            image (PIL.Image): An the Image object to turn into a DensePixelMatrix

        Returns:
            A built DensePixelMatrix
        """
        pixel_matrix = ptg.DensePixelMatrix(image.width, image.height, default="black")

        for horizontal in range(pixel_matrix.rows):
            for pixel in range(pixel_matrix.columns):
                pixel_value = image.getpixel((pixel, horizontal))

                if len(pixel_value) < 4:
                    r, g, b = pixel_value
                    pixel_matrix[horizontal, pixel] = f"{r};{g};{b}"
                else:
                    r, g, b, a = pixel_value

                    if a < 255:
                        pass
                    else:
                        pixel_matrix[horizontal, pixel] = f"{r};{g};{b}"

        pixel_matrix.build()

        return pixel_matrix

    def _inject_images(self):
        """
        Iterates through a scroll's content to find embedded image. Replaces it with the proper pixel matrix widget.
        """
        for page, scroll_content in self._scroll.content.items():
            for content in scroll_content:
                index = scroll_content.index(content)
                content_split = content.split(":")
                if content_split[0] == "IMGFILE":
                    image = self._scroll.images.get(content_split[1])
                    image_widget = self._build_embed_image(image)
                    content = image_widget

                scroll_content[index] = content
            self._scroll.content.update({page: scroll_content})

    def _get_section_content(self) -> list[str]:
        """
        Returns current page's corresponding content list from scroll's content dictionary.
        """

        return self._scroll.content.get(self.current_page)

    def _turn_page(self, page: int) -> None:
        """
        Turns the currently opened scroll to the given page.

        Args:
            page (int): Page to turn to
        """
        if page <= self.scroll_length and page > 0:
            self.current_page = page

        self._update_content()

    def _update_content(self) -> None:
        """
        Sets the ScrollReader's content viewer and page turning widgets.
        """
        content_viewer = ptg.Container(
            *self._get_section_content(),
            overflow=ptg.Overflow.SCROLL,
            parent_align=ptg.HorizontalAlignment.CENTER,
            height=20,
            box="EMPTY",
        )

        page_turner = ptg.Splitter(
            ["<", lambda *_: self._turn_page(self.current_page - 1)],
            f"{self.current_page}/{self.scroll_length}",
            [">", lambda *_: self._turn_page(self.current_page + 1)],
        )

        self.set_widgets([content_viewer, page_turner])
