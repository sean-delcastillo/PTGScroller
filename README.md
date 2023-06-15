# PTGScroller
## Terminal User Interface eReader

PTGScroller reads scroll files with the ".scrl" extension and displays the contents in the terminal using PyTermGUI

## Installation

TODO this section

## Usage
### Examples
#### ScrollLibrary Widget

```py
from scroller.widgets import ScrollLibrary
import pytermgui as ptg

with ptg.WindowManager() as manager:
    library = ScrollLibrary(manager)
    exit = ptg.Button("X", lambda *_: window.close())
    window = ptg.Window(exit, library).set_title(library.library_name)

    manager.add(window)
```

Import the Library class from scroller to build a library instance from a directory. Pass the WindowManager to the ScrollLibrary class
to build the library window. This example can be found in scripts/scrolllibrary_example.py.

#### Scrollmake

Scrollmake is a command-line tool to make scroll files. You can point the script at a directory with a content xml and image media to create the scroll file.
Please see the module for usage information.