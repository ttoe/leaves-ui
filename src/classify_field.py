import multiprocessing
import os     as os
import pandas as pd
import numpy  as np
from   glob   import glob
from   joblib import Parallel, delayed
from   skimage.io         import imread
from   skimage.measure    import label, regionprops


# region_filter :: Region -> Boolean
def region_filter(region):
    # main concern here is that the key regions are included
    # those are usually rectangular
    # therefore extent is the most reliable metric to filter by
    return (region.extent <= 0.8)


# filter_regions_by_props :: [Region] -> [Region]
def filter_regions_by_props(regions):
    return list(filter(region_filter, regions))


# get_region_props_df :: LabelledImage -> String -> DataFrame
def get_leaf_props_df(labelled_im, species_name):

    # getting region's properties and filtering by extent
    regions_properties = regionprops(labelled_im, cache=True)
    filtered_regions = filter_regions_by_props(regions_properties)

    # creating dataframe
    df = pd.DataFrame(columns=["species", "eccentricity", "extent", "solidity", "roundness"])

    if len(filtered_regions) == 1:
        # getting the props for the only region
        p = filtered_regions[0]

        # manually calculating roundness
        roundness = 4 * np.pi * p.area / p.perimeter**2

        # appending data to dataframe
        df.loc[len(df)+1] = [species_name, p.eccentricity, p.extent, p.solidity, roundness]

    return df


# process_field_images_dir :: String -> String -> DataFrame
def process_field_images_dir(root_dir, species_name):

    # get image filenames as a list and map image processing over it
    image_filenames = glob(root_dir + species_name + "/*.png")
    images = map(lambda im: label(imread(im)), image_filenames)

    # map over images in the current directory
    dir_dataframes = map(lambda image: get_leaf_props_df(image, species_name), images)

    return pd.concat(dir_dataframes)


# root of the directories with species lab images
root_dir = "/Users/totz/Desktop/leaves/leafsnap-dataset/selected_field/"

# get a list of all species (subdirectories)
species = [x[1] for x in os.walk(root_dir)][0]

# compute the results
results = Parallel(n_jobs=1)(delayed(process_field_images_dir)(root_dir, s) for s in species)


# aggregate the results in one dataframe
unknowns = pd.concat(results).sort_values(by="species")


# reading the precomputed data, that was saved as csv
data = pd.read_csv("../out/leaf_morphometrics_4beeeb7.csv", sep=";", decimal=",")

# selected species for which the assignment will be done
species = [ "abies_concolor", "acer_palmatum", "acer_saccharinum", "aesculus_glabra"
          , "amelanchier_arborea", "betula_populifolia", "juglans_nigra"
          , "metasequoia_glyptostroboides", "robinia_pseudo-acacia", "zelkova_serrata"]

# extracting the rows specified by 'species'
selected_species = data.loc[data["species"].isin(species)]

# calculating the medians of the morphometric descriptors per species
selected_species_medians = selected_species.groupby("species").median()


def calc_stats(unknown_species_df, species_centerpoints_df):
    uk = unknown_species_df.copy()
    gms = species_centerpoints_df.copy()
    
    df = pd.DataFrame(columns=["actual_species", "assigned_species"])
    
    for row in uk.iterrows():
        s = row[1] # get df object out of tuple
        distances = np.sqrt( (gms.eccentricity-s.eccentricity)**2 
                                + (gms.extent-s.extent)**2 
                                + (gms.solidity-s.solidity)**2
                                + (gms.roundness-s.roundness)**2 ) / 2

        df.loc[len(df)+1] = [s.species, distances.idxmin()]

    return df

assigned       = calc_stats(unknowns, selected_species_medians)
count_per_spec = assigned.groupby("actual_species").count()
correct        = assigned[assigned.actual_species == assigned.assigned_species]
count_correct  = correct.groupby("actual_species").count()
percent_correct = count_correct / count_per_spec * 100

