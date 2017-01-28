import numpy              as np
import pandas             as pd
from   glob               import glob
from   skimage.filters    import threshold_otsu
from   skimage.io         import imread
from   skimage.morphology import binary_closing, remove_small_objects
from   skimage.measure    import label, regionprops


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
    leaf_grey = im[:600, :600, 1]

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
    df = pd.DataFrame(columns=["species", "eccentricity", "extent", "solidity", "roundness"])

    if len(filtered_regions) == 1:
        # getting the props for the only region
        p = filtered_regions[0]

        # manually calculating roundness
        roundness = 4 * np.pi * p.area / p.perimeter**2

        # appending data to dataframe
        df.loc[len(df)+1] = [species_name, p.eccentricity, p.extent, p.solidity, roundness]

    return df


# process_images_dir :: String -> String -> DataFrame
def process_images_dir(root_dir, species_name):

    # get image filenames as a list and map image processing over it
    image_filenames = glob(root_dir + species_name + "/*.jpg")
    images = map(lambda image: process_and_label_image(image, species_name), image_filenames)

    # map over images in the current directory
    dir_dataframes = map(lambda image: get_leaf_props_df(image, species_name), images)

    return pd.concat(dir_dataframes)
