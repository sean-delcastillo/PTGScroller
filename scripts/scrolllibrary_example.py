from scroller.widgets import ScrollLibrary
import pytermgui as ptg

with ptg.WindowManager() as manager:
    library = ScrollLibrary(manager)
    exit = ptg.Button("X", lambda *_: window.close())
    window = ptg.Window(exit, library).set_title(library.library_name)

    manager.add(window)
