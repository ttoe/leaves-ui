"""TabFrame module, exporting the TabFrame class."""

import tkinter     as tk
import tkinter.ttk as ttk

class TabFrame(object):
    """Frame holding the tabs which display different images."""
    def __init__(self, root):

        self.root = root
        self.frame = ttk.Frame(self.root, relief="ridge", borderwidth=2)

        # FRAME CONTENT
        self.image_tabs = ttk.Notebook(self.frame)
        self.original_tab = tk.Frame(self.image_tabs)
        self.segmented_tab = tk.Frame(self.image_tabs)
        self.labelled_tab = tk.Frame(self.image_tabs)
        self.image_tabs.add(self.original_tab, text="Original")
        self.image_tabs.add(self.segmented_tab, text="Segmented")
        self.image_tabs.add(self.labelled_tab, text="Labelled")

        self.image_tabs.pack()

    def get_frame(self):
        """Getter method to access the frame"""
        return self.frame
