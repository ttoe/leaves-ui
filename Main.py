from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

def getTkImage(file):
    return ImageTk.PhotoImage(Image.open(file))

# GLOBALS
image_files = "nothing yet"


# This is where we lauch the file manager bar.
def openFile():
    global image_files
    name = askopenfilename(initialdir="~",
                            title="Choose an image file")
    print(name)
    image_files = name

root = Tk()
root.geometry("1000x700+0+0")
root.title("Leaves UI")


# sub frames holding specific content
menuFrame = Frame(root)
tabFrame  = Frame(root)
infoFrame = Frame(menuFrame)

# MENU FRAME CONTENT
quitButton    = Button(menuFrame, text="Quit", command=quit)
openImgButton = Button(menuFrame, text="Open", command=openFile)


# TAB FRAME CONTENT

imageTabs = Notebook(tabFrame)
t1 = Frame(imageTabs)
t2 = Frame(imageTabs)
t3 = Frame(imageTabs)
imageTabs.add(t1, text="Original")
imageTabs.add(t2, text="Segmented")
imageTabs.add(t3, text="Labelled")


lena = getTkImage("lena.jpg")
test = Label(t1, image=lena)


var = StringVar()
var.set(image_files)


# INFO FRAME CONTENT
info1 = Label(infoFrame, textvariable=var)
info2 = Label(infoFrame, text="info2")
info3 = Label(infoFrame, text="info3")

####### LAYOUT #######

## Frames
menuFrame.pack(side=LEFT, expand=False, fill=BOTH)
tabFrame.pack(side=RIGHT, expand=True, fill=BOTH)
infoFrame.pack(side=BOTTOM, expand=False, fill=X)

## Menu Frame
openImgButton.pack(fill=X)
info1.pack()
info2.pack()
info3.pack()
quitButton.pack(fill=X)

### Tab Frame
imageTabs.pack()
test.pack()

root.mainloop()
