import tkinter as tk
import tkinter.ttk as ttk
import sys

import BaseApp   as BA
import MenuFrame as MF
import TabFrame  as TF
import InfoFrame as IF


if __name__ == "__main__":
    root = tk.Tk()
    app  = BA.BaseApp(root)
    app.mainloop()
