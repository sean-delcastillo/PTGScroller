# PTG Scroller

PTG Scroller is an Terminal User Interface (TUI) e-reader library for reading .scrl ("Scroll") files using Balázs Cene's Python TUI framework [PyTermGUI](https://ptg.bczsalba.com/).

```termage-svg title=PTGScroller width=93 height=35
import pytermgui as ptg
from ptgscroller import ScrollReader, Library

with ptg.WindowManager() as manager:
    library = Library()

    positions = [(2, 2), (42, 12)]
    windows = []

    for position in positions:
        reader = ScrollReader(library, "Scroll Test")
        reader._turn_page(positions.index(position) + 1)
        reader = ptg.Window(reader)
        reader.width = 50
        reader.pos = position
        windows.append(reader)

    for window in windows:
        manager.add(window)
```

## Using PTG Scroller
Start by reading through the [tutorials](tutorials.md) for the fastest way to set up PTG Scroller by using the ScrollLibrary widget.