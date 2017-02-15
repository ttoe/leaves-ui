class TabFrame():
    def __init__(self, root):

        self.frame = ttk.Frame(root, width=500, height=500)
        self.frame.pack(side="bottom", fill="both", expand=True)

    def getFrame(self):
        return(self.frame)
