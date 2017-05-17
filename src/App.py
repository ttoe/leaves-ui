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
from   tkinter.filedialog   import askdirectory, asksaveasfilename
from   PIL                  import ImageTk, Image

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
        self.menu_frame = ttk.Frame(self.root, relief="ridge", borderwidth=1)
        self.tab_frame  = ttk.Frame(self.root, relief="ridge", borderwidth=1)
        self.button_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=1)
        self.drop_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=1)
        self.info_frame = ttk.Frame(self.menu_frame, relief="ridge", borderwidth=1)

        # MAIN FRAMES - PACKING
        self.menu_frame.pack(side="left", fill="both", expand=False, padx=2, pady=2)
        self.tab_frame.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        self.button_frame.pack(fill="x", expand=False, padx=2, pady=2)
        self.drop_frame.pack(fill="x", expand=False, padx=2, pady=2)
        self.info_frame.pack(fill="x", expand=False, padx=2, pady=2)

        # MENU FRAME CONTENT
        ttk.Button(self.button_frame, text="Select directory", command=self.get_dir_filenames).pack(side="left")
        ttk.Button(self.button_frame, text="Quit", command=quit).pack(side="right")

        # DROP DOWN MENU
        ttk.Button(self.drop_frame, text="<", width=1, command=self.select_previous).pack(side="left")
        ttk.Button(self.drop_frame, text=">", width=1, command=self.select_next).pack(side="right")

        self.drop = tk.OptionMenu(self.drop_frame,
                                  self.selected_image,
                                  *self.directory_filenames,
                                  command=self.process_selected)
        self.drop["width"] = 30
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

        # SAVE BUTTON
        ttk.Button(self.info_frame, text="Save image", command=self.save_current_tab_image).pack()

        # IMAGE LABELS - filled when loading an image
        self.original_image  = ttk.Label(self.original_tab)
        self.greyscale_image = ttk.Label(self.original_tab)
        self.segmented_image = ttk.Label(self.segmented_tab)
        self.labelled_image  = ttk.Label(self.labelled_tab)

        # RUN WHEN INSTANCE CREATED
        self.root.mainloop()

    # HELPER FUNCTIONS

    def select_previous(self):
        """missing docstring"""

        selected_index = self.directory_filenames.index(self.selected_image.get())

        if (selected_index > 0):
            new_selected_image = self.directory_filenames[selected_index - 1]
            self.selected_image.set(new_selected_image)
            self.process_selected(self.selected_image.get())


    def select_next(self):
        """missing docstring"""

        num_files = len(self.directory_filenames)
        selected_index = self.directory_filenames.index(self.selected_image.get())

        if (num_files - 1 > selected_index):
            new_selected_image = self.directory_filenames[selected_index + 1]
            self.selected_image.set(new_selected_image)
            self.process_selected(self.selected_image.get())


    def get_dir_filenames(self):
        """missing docstring"""

        images_dir = askdirectory(title="Choose image directory", mustexist=True)
        image_names = glob.glob(images_dir+"/*.*")

        self.directory_filenames = image_names
        self.selected_image.set(image_names[0])

        # update drop down
        self.drop.destroy()
        self.drop = tk.OptionMenu(self.drop_frame,
                                  self.selected_image,
                                  *self.directory_filenames,
                                  command=self.process_selected)
        self.drop["width"] = 30
        self.drop.pack()

        self.process_selected(self.selected_image.get())


    # display_images_and_data :: ImageFilePath -> IO ()
    def display_images_and_data(self, file_path):
        """missing docstring"""

        processed_image_object = iu.processing_pipe(file_path)

        self.pil_original_image     = Image.fromarray(processed_image_object["original_img"], "RGB")
        self.pil_greyscale_image    = Image.fromarray(processed_image_object["greyscale_img"], "L")
        self.pil_segmented_image    = Image.fromarray(processed_image_object["segmented_ubyte_img_bw"])
        self.pil_labelled_image     = Image.fromarray(processed_image_object["labelled_ubyte_img_rbg"], "RGB")

        regions_properties     = processed_image_object["regions_properties"] 

        # scaling the images
        frame_width  = int(self.tab_frame.winfo_width() * 0.9)
        frame_height = int(self.tab_frame.winfo_height() * 0.9)
        max_size     = (frame_width, frame_height)

        self.pil_original_image.thumbnail(max_size)
        self.pil_greyscale_image.thumbnail(max_size)
        self.pil_segmented_image.thumbnail(max_size)
        self.pil_labelled_image.thumbnail(max_size)

        # Filling the prepared image labels
        self.original_image_file  = ImageTk.PhotoImage(self.pil_original_image)
        self.greyscale_image_file = ImageTk.PhotoImage(self.pil_greyscale_image)
        self.segmented_image_file = ImageTk.PhotoImage(self.pil_segmented_image)
        self.labelled_image_file  = ImageTk.PhotoImage(self.pil_labelled_image)

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

        self.display_images_and_data(selection)

    def save_current_tab_image(self):
        current_tab = self.image_tabs.tab(self.image_tabs.select(), "text")
        print(current_tab)
        save_file_name = asksaveasfilename(defaultextension="bmp", title="Save currently displayed image")

        if   current_tab == "Original":
            self.pil_original_image.save(save_file_name)
        elif current_tab == "Greyscale":
            self.pil_greyscale_image.save(save_file_name)
        elif current_tab == "Segmented":
            self.pil_segmented_image.save(save_file_name)
        else:
            self.pil_labelled_image.save(save_file_name)

# RUN THE APP
BaseApp()
