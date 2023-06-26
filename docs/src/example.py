import pytermgui as ptg
from ptgscroller import ScrollReader, Library

with ptg.WindowManager() as manager:
    library = Library()

    positions = [(0, 0), (50, 50), (100, 100)]
    windows = []

    for position in positions:
        reader = ScrollReader(library, "Scroll Test")
        reader._turn_page(positions.index(position) + 1)
        reader = ptg.Window(reader)
        reader.width = 100
        reader.pos = position
        windows.append(reader)

    for window in windows:
        manager.add(window)
