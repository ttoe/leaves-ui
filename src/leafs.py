
# coding: utf-8


get_ipython().magic('matplotlib inline')
import warnings
warnings.filterwarnings("ignore")

import multiprocessing

import numpy              as np
import pandas             as pd
import os                 as os

from   glob               import glob
from   joblib             import Parallel, delayed
from   skimage.color      import rgb2grey, label2rgb
from   skimage.filter     import threshold_otsu, rank
from   skimage.io         import imread, imsave, imshow
from   skimage.measure    import label, regionprops
from   skimage.morphology import binary_closing, square, remove_small_objects, disk
from   skimage.util       import img_as_uint



# prop_filter_predicate :: Region -> Boolean
def region_filter(region):
    # main concern here is that the key regions are included
    # those are usually rectangular
    # therefore extent is the most reliable metric to filter by
    return (region.extent <= 0.8)



# filter_regions_by_props :: [Region] -> [Region]
def filter_regions_by_props(regions):
    return list(filter(region_filter, regions))



# get_leaf_props :: Image -> String -> LabelledImage
def process_and_label_image(image, species_name):
    
    # reading data
    im = imread(image)
    
    # cropping out the interesting part and just using green channel
    leaf_grey = im[:600,:600,1]
    
    # segmenting
    global_thresh = threshold_otsu(leaf_grey)

    # filling holes
    bw_closed = binary_closing(np.invert(leaf_grey > global_thresh))

    # removing small objects outside of leaf
    bw_closed_rem = remove_small_objects(bw_closed, min_size=128, connectivity=2)

    # return labelled image
    return label(bw_closed_rem)



# get_region_props_df :: LabelledImage -> DataFrame
def get_leaf_props_df(labelled_im, species_name):
    
    # getting region's properties and filtering by extent
    regions_properties = regionprops(labelled_im, cache=True)
    filtered_regions = filter_regions_by_props(regions_properties)
                
    # creating dataframe
    df = pd.DataFrame(columns = ["species", "eccentricity", "extent", "solidity"])
    
    if len(filtered_regions) == 1:
        # getting the props for the only region
        p = filtered_regions[0]

        # appending data to dataframe
        df.loc[len(df)+1] = [species_name, p.eccentricity, p.extent, p.solidity]
    
    return df



# takes a species name, which is used to build up the directory name over which will be looped
# all *.jpg images in that directory will be processed and a dataframe containing
# several morphometric descriptors will be returned
# process_images_dir :: String -> String -> DataFrame
def process_images_dir(root_dir, species_name):
    
    # get image filenames as a list and map image processing over it
    image_filenames = glob(root_dir + species_name + "/*.jpg")
    images = map(lambda image: process_and_label_image(image, species_name), image_filenames)
    
    # map over images in the current directory
    dir_dataframes = map(lambda image: get_leaf_props_df(image, species_name), list(images)[:10])
        
    return pd.concat(dir_dataframes)



# removing output files, clean slate
if os.path.exists("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv"):
    os.remove("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv")
if os.path.exists("/Users/totz/Desktop/leafs/out/multiple_regions.txt"):
    os.remove("/Users/totz/Desktop/leafs/out/multiple_regions.txt")
    
# root of the directories with species lab images
root_dir = "/Users/totz/Desktop/leafs/leafsnap-dataset/dataset/images/lab/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# get the maximum number of cores available
num_cores = multiprocessing.cpu_count()

# compute the results
results = Parallel(n_jobs=num_cores, verbose=11)(delayed(process_images_dir)(root_dir, i) for i in species[:10])



# aggregate the results in one dataframe
all_results = pd.concat(results).sort("species", ascending=1)

# write data to disk
all_results.to_csv("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv", index=False, float_format="%.3f", decimal=",", sep=";")



#all_results.hist("extent", bins=20)
#all_results.hist("solidity", bins=20)
#all_results.hist("perimeter", bins=20)

