import pytermgui as ptg
from scroller.widgets import ScrollLibrary
from scroller.scroller import Library

library = Library()

with ptg.WindowManager() as manager:
    library_widget = ScrollLibrary(library, manager)
    window = ptg.Window(library_widget).set_title(library_widget.library_name)
    manager.add(window)
