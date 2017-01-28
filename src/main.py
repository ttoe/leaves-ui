import multiprocessing
import os     as os
import pandas as pd
from   glob   import glob
from   joblib import Parallel, delayed
from   leaves import process_images_dir


# removing output
if os.path.exists("/Users/totz/Desktop/leaves/out/leaf_morphometrics.csv"):
    os.remove("/Users/totz/Desktop/leaves/out/leaf_morphometrics.csv")

# root of the directories with species lab images
root_dir = "/Users/totz/Desktop/leaves/leafsnap-dataset/dataset/images/lab/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# get the maximum number of cores available
num_cores = multiprocessing.cpu_count()

# compute the results
results = Parallel(n_jobs=num_cores, verbose=11)(delayed(process_images_dir)(root_dir, i) for i in species[:5])


# aggregate the results in one dataframe
all_results = pd.concat(results).sort_values(by="species")

# write data to disk
all_results.to_csv("/Users/totz/Desktop/leaves/out/leaf_morphometrics.csv", index=False, float_format="%.3f", decimal=",", sep=";")
