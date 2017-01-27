import multiprocessing

import os as os
import pandas as pd

from glob import glob
from joblib import Parallel, delayed

from leafs import get_leaf_props_df, process_and_label_image


# process_images_dir :: String -> String -> DataFrame
def process_images_dir(root_dir, species_name):

    # get image filenames as a list and map image processing over it
    image_filenames = glob(root_dir + species_name + "/*.jpg")
    images = map(lambda image: process_and_label_image(image, species_name), image_filenames)

    # map over images in the current directory
    dir_dataframes = map(lambda image: get_leaf_props_df(image, species_name), images)

    return pd.concat(dir_dataframes)


# removing output
if os.path.exists("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv"):
    os.remove("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv")

# root of the directories with species lab images
root_dir = "/Users/totz/Desktop/leafs/leafsnap-dataset/dataset/images/lab/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# get the maximum number of cores available
num_cores = multiprocessing.cpu_count()

# compute the results
results = Parallel(n_jobs=num_cores, verbose=11)(delayed(process_images_dir)(root_dir, i) for i in species[:50])


# aggregate the results in one dataframe
all_results = pd.concat(results).sort("species", ascending=1)

# write data to disk
all_results.to_csv("/Users/totz/Desktop/leafs/out/leaf_morphometrics.csv", index=False, float_format="%.3f", decimal=",", sep=";")
