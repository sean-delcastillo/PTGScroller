import pytermgui as ptg
from widgets import ScrollLibrary
from scroller import Library

library = Library()

with ptg.WindowManager() as manager:
    window = ptg.Window(ScrollLibrary(library, manager))
    manager.add(window)
