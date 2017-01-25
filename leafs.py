
# coding: utf-8


get_ipython().magic('matplotlib inline')
import warnings
warnings.filterwarnings("ignore")

import numpy  as np
import pandas as pd
import os     as os
from glob               import glob
from skimage.color      import rgb2gray, label2rgb
from skimage.filter     import threshold_otsu
from skimage.io         import imread, imsave
from skimage.measure    import label, regionprops
from skimage.morphology import closing, square, remove_small_objects
from skimage.util       import img_as_uint



# root of the directories with species lab images
root_dir = "~/Desktop/leafs/leafsnap-dataset/dataset/images/lab/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# the region properties to be computed and stored
columns = [ "species", "area", "convex_area", "eccentricity", "equivalent_diameter", "extent"
          , "major_axis_length", "minor_axis_length", "perimerter", "solidity" ]

# creating dataframe
df = pd.DataFrame(columns=columns)

# loop over all subdirectories
for s in species:
    print(s)
    
    # get image filenames as a list
    images = glob(root_dir + s + "/*.jpg")
    
    # loop over all images in the current directory
    for i in images[:5]:
        
        # reading data
        im = io.imread(i)

        # cropping out the interesting part
        leaf_grey = rgb2gray(im[:600,:600])

        # segmenting
        thresh = threshold_otsu(leaf_grey)

        # filling holes
        bw_closed = binary_closing(np.invert(leaf_grey > thresh))

        # removing small objects outside of leaf
        bw_closed_rem = remove_small_objects(bw_closed, min_size=128, connectivity=2)

        # labelling
        labelled = label(bw_closed_rem)
        image_label_overlay = label2rgb(labelled, image=bw_closed_rem)

        # computing properties
        props = regionprops(labelled, cache=True)

        # looping over all regions
        for p in props:
            
            # extracting morphometric data from regionprops
            data = [s, p.area, p.convex_area, p.eccentricity, p.equivalent_diameter, p.extent
                   , p.major_axis_length, p.minor_axis_length, p.perimeter, p.solidity]

            # appending data to dataframe
            df.loc[len(df)+1] = data

df.to_csv("~/Desktop/leafs/leaf_morphometrics.csv", index=False, float_format="%.3f")

# saving
# io.imsave(f[:-4] + ".bmp", img_as_uint(bw_closed_rem))
# io.imsave(f[:-4] + "_label.bmp", image_label_overlay)
# io.imsave(f[:-4] + "_slice_bb.bmp", img_as_uint(p[0].image))

