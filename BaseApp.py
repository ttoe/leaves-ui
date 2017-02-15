import tkinter as tk
import tkinter.ttk as ttk
import sys


class BaseApp():

    def __init__(self, root):
        # BASIC
        root.title("Title")
        root.option_add('*tearOff', tk.FALSE)
        self.frame = ttk.Frame(root, width=500, height=500)
        self.frame.pack(side="top", fill="both", expand=True)

        # MENUBAR
        menubar = tk.Menu(root)
        self.menu=dict()
        self.menubar=menubar
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="Datei", underline=0)
        menu_file.add_command(label="Öffnen...",  command=self.openFile, underline=0)
        menu_file.add_command(label="Beenden", command=self.Exit,underline=1)
        root.config(menu=menubar)
        self.root=root
        self.menu["menubar"] = menubar
        self.menu["Datei"]   = menu_file

    def openFile(self):
        pass

    def Exit(self):
        sys.exit(0)

    def mainloop(self):
        self.root.mainloop()

    def getFrame(self):
        return(self.frame)
