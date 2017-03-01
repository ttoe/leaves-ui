"""missing docstring"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

from frames.MenuFrame import MenuFrame
from frames.TabFrame  import TabFrame
from frames.InfoFrame import InfoFrame


# BASE CLASS

class BaseApp(object):
    """missing docstring"""
    def __init__(self):
        # BASIC
        self.root = tk.Tk()
        self.root.title("Leaves UI")
        self.root.geometry("1000x700")
        self.frame = ttk.Frame(self.root, width=1000, height=700)
        self.frame.pack(side="top", fill="both", expand=True)

        # MENUBAR
        menubar = tk.Menu(self.root)
        self.menu = dict()
        self.menubar = menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="Datei", underline=0)
        menu_file.add_command(label="Oeffnen...", command=open_file, underline=0)
        menu_file.add_command(label="Beenden", command=quit, underline=1)
        self.root.config(menu=menubar)
        self.menu["menubar"] = menubar
        self.menu["Datei"] = menu_file

        # FRAMES
        self.menu_frame = MenuFrame(self.frame).getFrame()
        self.tab_frame = TabFrame(self.frame).get_frame()
        self.info_frame = InfoFrame(self.tab_frame).getFrame()

        self.menu_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        self.tab_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.info_frame.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

        # RUN IF INSTANCE CREATED
        self.root.mainloop()

    # put the loaded image into a tab
    # Label(self.tabFrame.imageTabs.originalTab, image=file_image).pack()

# FUNCTIONS

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
