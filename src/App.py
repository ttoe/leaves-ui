#!/usr/bin/env python

"""missing docstring"""

# Matplotlib import is a workaround for a c++ library problem
import matplotlib
matplotlib.use("TkAgg")

import tkinter     as tk
import tkinter.ttk as ttk
import skimage.io  as io
import numpy       as np
from   tkinter.filedialog import askopenfilename
from   PIL                import ImageTk, Image

# import custom functions
import img_utils as iu

# App
class BaseApp():
    """missing docstring"""
    def __init__(self):
        # BASIC
        self.root = tk.Tk()
        self.root.title("Leaves UI")
        self.root.geometry("1000x700")
        self.root.attributes('-fullscreen', True)
        self.frame = ttk.Frame(self.root, width=1000, height=700)
        self.frame.pack(side="top", fill="both", expand=True)

        # MAIN FRAMES
        self.menu_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.tab_frame = ttk.Frame(self.frame, relief="ridge", borderwidth=2)
        self.info_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=2)

        # MAIN FRAMES - PACKING
        self.menu_frame.pack(side="left", fill="both", expand=False, padx=5, pady=5)
        self.tab_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.info_frame.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

        # ADDING FRAME LABELS /// temp ///
        # ttk.Label(self.info_frame, text="info frame").pack()
        # ttk.Label(self.menu_frame, text="menu frame").pack()

        # MENU FRAME CONTENT
        open_button = ttk.Button(self.menu_frame, text="Open", command=self.open_file).pack()
        quit_button = ttk.Button(self.menu_frame, text="Quit", command=quit).pack()

        # TAB FRAME CONTENT
        self.image_tabs = ttk.Notebook(self.tab_frame)
        self.original_tab = tk.Frame(self.image_tabs)
        self.segmented_tab = tk.Frame(self.image_tabs)
        self.labelled_tab = tk.Frame(self.image_tabs)
        self.image_tabs.add(self.original_tab, text="Original")
        self.image_tabs.add(self.segmented_tab, text="Segmented")
        self.image_tabs.add(self.labelled_tab, text="Labelled")
        self.image_tabs.pack()

        # IMAGE LABELS - to be filled later
        self.original_image = ttk.Label(self.original_tab)
        self.segmented_image = ttk.Label(self.segmented_tab)
        self.labelled_image = ttk.Label(self.labelled_tab)

        # RUN WHEN INSTANCE CREATED
        self.root.mainloop()

    # HELPER FUNCTIONS

    def open_file(self):
        """missing docstring"""
        image_path = askopenfilename(title="Choose an image file")
        
        processed_images    = iu.processing_pipe(image_path)

        original_image      = processed_images["original_img"]
        segmented_image     = processed_images["segmented_ubyte_img_bw"]
        labelled_image      = processed_images["labelled_ubyte_img_rbg"]

        pil_original_image  = Image.fromarray(original_image, "RGB")
        pil_segmented_image = Image.fromarray(segmented_image)
        pil_labelled_image  = Image.fromarray(labelled_image, "RGB")

        im_width, im_height = pil_original_image.size
        frame_width  = int(self.tab_frame.winfo_width() * 0.9)
        frame_height = int(self.tab_frame.winfo_height() * 0.9)

        # if the image is larger than it's containing frame it's rescaled
        wh_ratio = im_width / im_height
        new_width, new_height = frame_width, frame_height
        if (im_width > frame_width) or (im_height > frame_height):
            if wh_ratio > 1:
                new_h = int((new_width / im_width) * im_height)
            else:
                new_w = int((new_height / im_height) * im_width)
        size = (new_width, new_height)

        self.original_image_file  = ImageTk.PhotoImage(pil_original_image.resize(size))
        self.segmented_image_file = ImageTk.PhotoImage(pil_segmented_image.resize(size))
        self.labelled_image_file  = ImageTk.PhotoImage(pil_labelled_image.resize(size))

        # DESTROY CURRENT IMAGES AND DISPLAY NEW ONES

        self.original_image.destroy()
        self.original_image = ttk.Label(self.original_tab, image=self.original_image_file)
        self.original_image.pack()

        self.segmented_image.destroy()
        self.segmented_image = ttk.Label(self.segmented_tab, image=self.segmented_image_file)
        self.segmented_image.pack()

        self.labelled_image.destroy()
        self.labelled_image = ttk.Label(self.labelled_tab, image=self.labelled_image_file)
        self.labelled_image.pack()


    def get_new_img_sizes(width, height):
        pass

# RUN THE APP
BaseApp()
