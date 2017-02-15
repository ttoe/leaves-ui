class MenuFrame():
    def __init__(self, root):

        self.frame = ttk.Frame(root, width=500, height=500)
        self.frame.pack(side="left", fill="both", expand=False)

    def getFrame(self):
        return(self.frame)
