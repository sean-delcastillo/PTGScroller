## How to Customize ScrollReader Instances Opened by ScrollLibrary
The size of images embedded into the textual content of a scroll can be controlled by passing an `embed_size` attribute to the ScrollReader's constructor. 

However, for most usecases the ScrollReader widget is opened via an already instanced ScrollLibrary. You can pass the keyword argument `embed_size` to a ScrollLibrary's constructor; this will affect all ScrollReader objects opened by this ScrollLibrary instance. 

```python
from scroller.widgets import ScrollLibrary
import pytermgui as ptg

with ptg.WindowManager() as manager:
    library = ScrollLibrary(manager, embed_size=16) # Set embedded image size to 16x16 pixels
    exit = ptg.Button("X", lambda *_: window.close())
    window = ptg.Window(exit, library).set_title(library.library_name).center()

    manager.add(window)
```