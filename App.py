import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

from frames.MenuFrame import MenuFrame
from frames.TabFrame  import TabFrame
from frames.InfoFrame import InfoFrame


class BaseApp(object):
    def __init__(self):
        # BASIC
        self.root = tk.Tk()
        self.root.title("Leaves UI")
        self.root.geometry("1000x700")
        self.frame = ttk.Frame(self.root, width=1000, height=700)
        self.frame.pack(side="top", fill="both", expand=True)
        
        # MENUBAR
        menubar = tk.Menu(self.root)
        self.menu=dict()
        self.menubar=menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="Datei", underline=0)
        menu_file.add_command(label="Öffnen...", command=self.openFile, underline=0)
        menu_file.add_command(label="Beenden", command=quit, underline=1)
        self.root.config(menu=menubar)
        self.menu["menubar"] = menubar
        self.menu["Datei"]   = menu_file

        # FRAMES    
        menuFrame = MenuFrame(self.frame)
        tabFrame  = TabFrame(self.frame)
        infoFrame = InfoFrame(tabFrame.getFrame())
        
        menuFrame.getFrame().pack(side="left", fill="both", expand=False, padx=5, pady=5)
        tabFrame.getFrame().pack(side="right", fill="both", expand=True, padx=5, pady=5)
        infoFrame.getFrame().pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

        # RUN IF INSTANCE CREATED
        self.root.mainloop()

    def openFile(self):
        name = askopenfilename(initialdir="~", title="Choose an image file")
        print(name)

    def getTkImage(file):
        return ImageTk.PhotoImage(Image.open(file))


# RUN THE APP
app = BaseApp()
