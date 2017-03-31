"""missing docstring"""

from   skimage.filters    import threshold_otsu
from   skimage.io         import imread
from   skimage.morphology import binary_closing, remove_small_objects
from   skimage.measure    import label, regionprops
import numpy              as np
import pandas             as pd


# region_filter :: Region -> Boolean
def region_filter(region):
    """missing docstring"""
    # main concern here is that the key regions are included
    # those are usually rectangular
    # therefore extent is the most reliable metric to filter by
    return region.extent <= 0.8


# filter_regions_by_props :: [Region] -> [Region]
def filter_regions_by_props(regions):
    """missing docstring"""
    return list(filter(region_filter, regions))


# original_to_segmented :: String -> Img
def original_to_segmented(file_path):
    """missing docstring"""

    # reading data
    img = imread(file_path)

    # cropping out the interesting part and just using green channel
    # leaf_grey = img[:600, :600, 1]
    greyscale_image = img[:600, :600, 1]

    # segmenting
    global_thresh = threshold_otsu(greyscale_image)

    # filling holes
    bw_closed = binary_closing(np.invert(greyscale_image > global_thresh))

    # removing small objects outside of leaf
    bw_closed_rem = remove_small_objects(bw_closed, min_size=128, connectivity=2)

    return bw_closed_rem


# segmented_to_labelled :: Image -> Image
def segmented_to_labelled(img):
    """missing docstring"""
    return label(img)


# labelled_to_filtered :: Image -> Image
def labelled_to_filtered(img): # , species_name
    """missing docstring"""
    # getting region's properties and filtering by extent
    regions_properties = regionprops(img, cache=True)
    filtered_regions = filter_regions_by_props(regions_properties)

    # creating dataframe
    dataframe = pd.DataFrame(columns=["eccentricity", #"species",
                                      "extent", "solidity", "roundness"])

    if len(filtered_regions) == 1:
        # getting the props for the only region
        props = filtered_regions[0]

        # manually calculating roundness
        roundness = 4 * np.pi * props.area / props.perimeter**2

        # appending data to dataframe
        dataframe.loc[len(dataframe)+1] = [props.eccentricity, # species_name,
                                           props.extent, props.solidity, roundness]

    return dataframe
