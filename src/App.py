"""missing docstring"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

class BaseApp():
    """missing docstring"""
    def __init__(self):
        # BASIC
        self.root = tk.Tk()
        self.root.title("Leaves UI")
        self.root.geometry("1000x700")
        self.frame = ttk.Frame(self.root, width=1000, height=700)
        self.frame.pack(side="top", fill="both", expand=True)

        # MENUBAR
        self.menubar = tk.Menu(self.root)
        self.menu = dict()
        # self.menubar = menubar
        self.menu_file = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="Datei", underline=0)
        self.menu_file.add_command(label="Oeffnen...", command=self.open_file, underline=0)
        self.menu_file.add_command(label="Beenden", command=quit, underline=1)
        self.root.config(menu=self.menubar)
        self.menu["menubar"] = self.menubar
        self.menu["Datei"] = self.menu_file

        # MAIN FRAMES
        self.menu_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.tab_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.info_frame = ttk.Frame(self.tab_frame, relief="ridge", borderwidth=2)

        # PACKING THE MAIN FRAMES
        self.menu_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        self.tab_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.info_frame.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

        # ADDING FRAME LABELS
        ttk.Label(self.info_frame, text="info frame").pack()
        ttk.Label(self.menu_frame, text="menu frame").pack()

        # TAB FRAME CONTENT
        self.image_tabs = ttk.Notebook(self.tab_frame)
        self.original_tab = tk.Frame(self.image_tabs)
        self.segmented_tab = tk.Frame(self.image_tabs)
        self.labelled_tab = tk.Frame(self.image_tabs)
        self.image_tabs.add(self.original_tab, text="Original")
        self.image_tabs.add(self.segmented_tab, text="Segmented")
        self.image_tabs.add(self.labelled_tab, text="Labelled")
        self.image_tabs.pack()

        # DEFAULT VALUES

        # initial image
        self.image_file = ImageTk.PhotoImage(
            Image.open("/Users/totz/Desktop/leaves-ui/img/init.jpg"))
        self.original_image = ttk.Label(self.original_tab, image=self.image_file)
        self.original_image.pack()

        # RUN WHEN INSTANCE CREATED
        self.root.mainloop()

    # HELPER FUNCTIONS

    def open_file(self):
        """missing docstring"""
        self.image_file = askopenfilename(initialdir="~/Desktop/leaves-ui/img",
                                          title="Choose an image file")

        im_width = int(self.tab_frame.winfo_width() * 0.8)
        im_height = int(self.tab_frame.winfo_height() * 0.8)
        self.image_file = ImageTk.PhotoImage(
            Image.open(self.image_file).resize((im_width, im_height)))

        self.original_image.destroy()
        self.original_image = ttk.Label(self.original_tab,
                                        image=self.image_file)
        self.original_image.pack()

# RUN THE APP
BaseApp()
