from typing import Any
import pytermgui as ptg
from scroller import Library


class ScrollLibrary(ptg.Container):
    def __init__(
        self, library: Library, window_manager: ptg.WindowManager, **attrs: Any
    ) -> None:
        super().__init__(**attrs)
        attrs.update({"box": "EMPTY"})
        self.library = library
        self.window_manager = window_manager

        self.update_content()

    def button_handler(self, scroll_title: str):
        title = scroll_title

        def draw_scroll_window(*_):
            reader = ScrollReader(self.library, title)

            window = ptg.Window(reader, width=100).center()

            self.window_manager.add(window)

        return draw_scroll_window

    def generate_library_buttons(self) -> list[ptg.Button]:
        library_buttons = []
        for title, scroll in self.library.scrolls.items():
            library_buttons.append([title, self.button_handler(title)])

        return library_buttons

    def update_content(self) -> None:
        buttons = ptg.Container(*self.generate_library_buttons(), box="EMPTY")

        self.set_widgets([buttons])


class ScrollReader(ptg.Container):
    def __init__(
        self,
        library: Library,
        scroll_title: str,
        **attrs: Any,
    ) -> None:
        super().__init__(**attrs)
        attrs.update({"box": "EMPTY"})
        self._scroll = library.find(scroll_title)
        self._scroll.open()
        self._current_page = 1
        self._scroll_length = len(self._scroll.content.keys())
        self.update_content()

    def get_section_content(self) -> list[str]:
        return self._scroll.content.get(self._current_page)

    def turn_page(self, page: int) -> None:
        if page <= self._scroll_length and page > 0:
            self._current_page = page

        self.update_content()

    def update_content(self) -> None:
        content_viewer = ptg.Container(
            *self.get_section_content(),
            overflow=ptg.Overflow.SCROLL,
            parent_align=ptg.HorizontalAlignment.CENTER,
            height=20,
            box="EMPTY",
        )

        page_turner = ptg.Splitter(
            ["<", lambda *_: self.turn_page(self._current_page - 1)],
            f"{self._current_page}/{self._scroll_length}",
            [">", lambda *_: self.turn_page(self._current_page + 1)],
        )

        self.set_widgets([content_viewer, page_turner])
