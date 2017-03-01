import tkinter.ttk as ttk

class MenuFrame():
    def __init__(self, root):

        self.frame = ttk.Frame(root, relief="ridge", borderwidth=2)

        # FRAME CONTENT
        info = ttk.Label(self.frame, text="menu frame")
        info.pack()

    def getFrame(self):
        return(self.frame)
