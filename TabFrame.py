import tkinter.ttk as ttk

class TabFrame():
    def __init__(self, root):

        self.frame = ttk.Frame(root, relief="ridge", borderwidth=2)#, width=500, height=500)
        # self.frame.pack(side="right", fill="both", expand=True)

        info = ttk.Label(self.frame, text="tab frame")
        info.pack()

    def getFrame(self):
        return(self.frame)
