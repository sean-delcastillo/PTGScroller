# PTGScroller
## Terminal User Interface eReader

PTGScroller reads scroll files with the ".scrl" extension and displays the contents in the terminal using PyTermGUI

## Installation

TODO this section

## Usage
### Example

```py
import pytermgui as ptg
from scroller.widgets import ScrollLibrary
from scroller.scroller import Library

library = Library() # The Library class's default library directory is "scroll-library"

with ptg.WindowManager() as manager:
    library_widget = ScrollLibrary(library, manager)
    window = ptg.Window(library_widget).set_title(library_widget.library_name)  # The ScrollLibrary instance has public attributes that can be accessed to style the window
    manager.add(window)
```

Import the Library class from scroller to build a library instance from a directory. Pass the WindowManager, and Library instances to the ScrollLibrary class
to build the library window. This example can be found in scripts/scrolllibrary_example.py.