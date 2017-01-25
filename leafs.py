
# coding: utf-8


get_ipython().magic('matplotlib inline')
import warnings
warnings.filterwarnings("ignore")

import multiprocessing
import numpy  as np
import pandas as pd
import os     as os

from joblib             import Parallel, delayed
from glob               import glob
from skimage.color      import rgb2gray, label2rgb
from skimage.filter     import threshold_otsu
from skimage.io         import imread, imsave
from skimage.measure    import label, regionprops
from skimage.morphology import binary_closing, square, remove_small_objects
from skimage.util       import img_as_uint


# get_leaf_props :: String -> String -> DataFrame
def get_leaf_props(image, species_name):

    # the region properties to be computed and stored
    columns = [ "species", "area", "convex_area", "eccentricity", "equivalent_diameter", "extent"
              , "major_axis_length", "minor_axis_length", "perimeter", "solidity" ]
    
    # creating dataframe
    df = pd.DataFrame(columns=columns)
    
    # reading data
    im = imread(image)
    
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
    # image_label_overlay = label2rgb(labelled, image=bw_closed_rem)

    # computing properties
    props = regionprops(labelled, cache=True)

    # looping over all regions
    # there should only ever be one region, but the image processing
    # pipeline is imperfect and there are still problems to fix here
    for p in props:
            
        # extracting morphometric data from regionprops
        data = [species_name, p.area, p.convex_area, p.eccentricity, p.equivalent_diameter, p.extent
               , p.major_axis_length, p.minor_axis_length, p.perimeter, p.solidity]

        # appending data to dataframe
        df.loc[len(df)+1] = data
    
    return df


# takes a species name, which is used to build up the directory name over which will be looped
# all *.jpg images in that directory will be processed and a dataframe containing
# several morphometric descriptors will be returned

# process_images_dir :: String -> String -> DataFrame
def process_images_dir(root_dir, species_name):

    # list to hold all dataframes, one per image
    res = []
    
    # get image filenames as a list
    images = glob(root_dir + species_name + "/*.jpg")
    
    # loop over all images in the current directory
    for i in images[:10]:
        
        # appending data to dataframe
        # df.loc[len(df)+1] = get_leaf_props(i, species_name)
        res += [get_leaf_props(i, species_name)]
        
    return pd.concat(res)



# root of the directories with species lab images
root_dir = "/Users/totz/Desktop/leafs/leafsnap-dataset/dataset/images/lab/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# get the maximum number of cores available
num_cores = multiprocessing.cpu_count() - 1

# compute the results
results = Parallel(n_jobs=num_cores, verbose=11)(delayed(process_images_dir)(root_dir, i) for i in species)



# aggregate the results in one dataframe
all_results = pd.concat(results).sort("species", ascending=1)

# write data to disk
all_results.to_csv("/Users/totz/Desktop/leafs/leaf_morphometrics.csv", index=False, float_format="%.3f")

