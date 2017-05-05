#!/usr/bin/env python

"""missing docstring"""

# Matplotlib import is a workaround for a c++ library problem
import matplotlib
matplotlib.use("TkAgg")

import tkinter              as tk
import tkinter.ttk          as ttk
import tkinter.scrolledtext as tkst
import glob                 as glob
import skimage.io           as io
import numpy                as np
from   tkinter.filedialog import askopenfilename, askdirectory
from   PIL                import ImageTk, Image
import PIL.Image as pi

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
        self.root.attributes("-fullscreen", True)

        self.directory_filenames = ["Load an image directory..."]
        self.selected_image = tk.StringVar()

        # MAIN FRAMES
        self.menu_frame = ttk.Frame(self.root, relief="ridge", borderwidth=2)
        self.tab_frame  = ttk.Frame(self.root, relief="ridge", borderwidth=2)
        self.button_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=2)
        self.drop_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=2)
        self.info_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=2)

        # MAIN FRAMES - PACKING
        self.menu_frame.pack(side="left", fill="both", expand=False, padx=2, pady=2)
        self.tab_frame.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        self.button_frame.pack(fill="x", expand=False, padx=2, pady=2)
        self.drop_frame.pack(fill="x", expand=False, padx=2, pady=2)
        self.info_frame.pack(fill="x", expand=False, padx=2, pady=2)

        # MENU FRAME CONTENT
        ttk.Button(self.button_frame, text="Select directory", command=self.get_dir_filenames).pack(side="left")
        ttk.Button(self.button_frame, text="Quit", command=quit).pack(side="left")

        # DROP DOWN MENU
        self.drop = tk.OptionMenu(self.drop_frame,
                                  self.selected_image,
                                  *self.directory_filenames,
                                  command=self.process_selected)
        # self.drop = tk.OptionMenu(self.drop_frame, self.selected_image, *self.directory_filenames, command)
        self.drop["width"] = 40
        self.drop.pack()

        # TAB FRAME CONTENT
        self.image_tabs = ttk.Notebook(self.tab_frame)
        self.original_tab = tk.Frame(self.image_tabs)
        self.greyscale_tab = tk.Frame(self.image_tabs)
        self.segmented_tab = tk.Frame(self.image_tabs)
        self.labelled_tab = tk.Frame(self.image_tabs)
        self.image_tabs.add(self.original_tab, text="Original")
        self.image_tabs.add(self.greyscale_tab, text="Greyscale")
        self.image_tabs.add(self.segmented_tab, text="Segmented")
        self.image_tabs.add(self.labelled_tab, text="Labelled")
        self.image_tabs.pack()

        # REGION DATA
        ttk.Label(self.info_frame, text="Region's properties").pack()
        self.region_data = tkst.ScrolledText(master=self.info_frame, height=10, width=47)
        self.region_data.pack()
        self.region_data.insert("1.0", "Please load an image...")

        # IMAGE LABELS - filled when loading an image
        self.original_image  = ttk.Label(self.original_tab)
        self.greyscale_image = ttk.Label(self.original_tab)
        self.segmented_image = ttk.Label(self.segmented_tab)
        self.labelled_image  = ttk.Label(self.labelled_tab)

        # RUN WHEN INSTANCE CREATED
        self.root.mainloop()

    # HELPER FUNCTIONS

    def get_dir_filenames(self):
        """missing docstring"""

        images_dir = askdirectory(title="Choose image directory", mustexist=True)
        image_names = glob.glob(images_dir+"/*.*")

        self.directory_filenames = image_names 

        # update drop down
        # !!! das muss anders gehen !!!
        self.drop.destroy()
        self.drop = tk.OptionMenu(self.drop_frame,
                                  self.selected_image,
                                  *self.directory_filenames,
                                  command=self.process_selected)
        self.drop["width"] = 40
        self.drop.pack()

#         self.selected_image.set("")
#         self.drop["menu"].delete(0, "end")
#         for option in image_names:
#             self.drop["menu"].add_command(label=option, command=tk._setit(self.selected_image, option))
#         self.drop["menu"].add_command(command=self.process_selected)


    # display_images_and_data :: ImageFilePath -> IO ()
    def display_images_and_data(self, file_path):
        """missing docstring"""

        processed_image_object = iu.processing_pipe(file_path)

        pil_original_image     = Image.fromarray(processed_image_object["original_img"], "RGB")
        pil_greyscale_image    = Image.fromarray(processed_image_object["greyscale_img"], "L")
        pil_segmented_image    = Image.fromarray(processed_image_object["segmented_ubyte_img_bw"])
        pil_labelled_image     = Image.fromarray(processed_image_object["labelled_ubyte_img_rbg"], "RGB")

        regions_properties     = processed_image_object["regions_properties"] 

        # scaling the images
        frame_width  = int(self.tab_frame.winfo_width() * 0.9)
        frame_height = int(self.tab_frame.winfo_height() * 0.9)
        max_size     = (frame_width, frame_height)

        pil_original_image.thumbnail(max_size)
        pil_greyscale_image.thumbnail(max_size)
        pil_segmented_image.thumbnail(max_size)
        pil_labelled_image.thumbnail(max_size)

        # Filling the prepared image labels
        self.original_image_file  = ImageTk.PhotoImage(pil_original_image)
        self.greyscale_image_file = ImageTk.PhotoImage(pil_greyscale_image)
        self.segmented_image_file = ImageTk.PhotoImage(pil_segmented_image)
        self.labelled_image_file  = ImageTk.PhotoImage(pil_labelled_image)

        # DESTROY CURRENT IMAGES AND DISPLAY NEW ONES

        self.original_image.destroy()
        self.original_image = ttk.Label(self.original_tab, image=self.original_image_file)
        self.original_image.pack()

        self.greyscale_image.destroy()
        self.greyscale_image = ttk.Label(self.greyscale_tab, image=self.greyscale_image_file)
        self.greyscale_image.pack()

        self.segmented_image.destroy()
        self.segmented_image = ttk.Label(self.segmented_tab, image=self.segmented_image_file)
        self.segmented_image.pack()

        self.labelled_image.destroy()
        self.labelled_image = ttk.Label(self.labelled_tab, image=self.labelled_image_file)
        self.labelled_image.pack()


        # show region properties
        self.region_data.replace(1.0, tk.END, regions_properties)


    def process_selected(self, selection):
        """missing docstring"""

        # self.display_images_and_data(self.selected_image.get())
        self.display_images_and_data(selection)

# RUN THE APP
BaseApp()
