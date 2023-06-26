### Using ScrollLibrary to Display Scroll Files for Selection

In this tutorial we will begin working with PTGScroller by initializing the ScrollLibrary class and rendering the widget using PyTermGUI.

First create a project directory, for example, called `ScrollTutorial`. Then create a subdirectory called `scroll-library`.

Download and copy over the files in the repo's own `scroll-library` directory. These should be called `readme.scrl` and `test_scroll.scrl`.

In the root project directory create a Python module named `scrolllibrary_example.py` with the following contents:

```python
from scroller.widgets import ScrollLibrary
import pytermgui as ptg

with ptg.WindowManager() as manager:
    library = ScrollLibrary(manager)
    exit = ptg.Button("X", lambda *_: window.close())
    window = ptg.Window(exit, library).set_title(library.library_name).center()

    manager.add(window)
```

The directory should look like:

```
ScrollTutorial
┝ scrolllibrary_example.py
└ scroll_library
  ┝ readme.scrl
  ┕ test_scroll.scrl
```

Running `scrolllibrary_example.py` should result in the following terminal output:

```termage-svg title=scrolllibrary_example.py
from scroller.widgets import ScrollLibrary
import pytermgui as ptg

with ptg.WindowManager() as manager:
    library = ScrollLibrary(manager)
    exit = ptg.Button("X", lambda *_: window.close())
    window = ptg.Window(exit, library).set_title(library.library_name).center()

    manager.add(window)
```

Notice that the ScrollLibrary widget does not display the scroll's file name. Instead the widget parses through the scroll file's contents and displays the scroll's title attribute instead.

Clicking on either title button will render the ScrollReader widget with the selected scroll's contents.

Congratulations! You just used PTGScroller's ScrollLibrary widget to parse through a library directory to find scroll files to read.