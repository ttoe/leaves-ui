"""missing docstring"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

# BASE CLASS

class BaseApp():
    """missing docstring"""
    def __init__(self):
        # BASIC
        root = tk.Tk()
        root.title("Leaves UI")
        root.geometry("1000x700")
        frame = ttk.Frame(root, width=1000, height=700)
        frame.pack(side="top", fill="both", expand=True)

        # MENUBAR
        menubar = tk.Menu(root)
        menu = dict()
        menubar = menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="Datei", underline=0)
        menu_file.add_command(label="Oeffnen...", command=open_file, underline=0)
        menu_file.add_command(label="Beenden", command=quit, underline=1)
        root.config(menu=menubar)
        menu["menubar"] = menubar
        menu["Datei"] = menu_file

        # MAIN FRAMES
        menu_frame = ttk.Frame(frame, relief="ridge", borderwidth=2)
        tab_frame = ttk.Frame(frame, relief="ridge", borderwidth=2)
        info_frame = ttk.Frame(tab_frame, relief="ridge", borderwidth=2)

        # PACKING THE MAIN FRAMES
        menu_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        tab_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        info_frame.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

        # ADDING FRAME LABELS
        ttk.Label(info_frame, text="info frame").pack()
        ttk.Label(menu_frame, text="menu frame").pack()
        ttk.Label(tab_frame, text="tab frame").pack()

        # TAB FRAME CONTENT
        image_tabs = ttk.Notebook(tab_frame)
        original_tab = tk.Frame(image_tabs)
        segmented_tab = tk.Frame(image_tabs)
        labelled_tab = tk.Frame(image_tabs)
        image_tabs.add(original_tab, text="Original")
        image_tabs.add(segmented_tab, text="Segmented")
        image_tabs.add(labelled_tab, text="Labelled")
        image_tabs.pack()

        # RUN IF INSTANCE CREATED
        root.mainloop()

        # put the loaded image into a tab
        # Label(self.tabFrame.imageTabs.originalTab, image=file_image).pack()

# HELPER FUNCTIONS

def get_tk_image(filename):
    """missing docstring"""
    return ImageTk.PhotoImage(Image.open(filename))

def open_file():
    """missing docstring"""
    file_name = askopenfilename(initialdir="~", title="Choose an image file")
    file_image = get_tk_image(file_name)

    print(file_name)
    return file_image

# RUN THE APP
BaseApp()
