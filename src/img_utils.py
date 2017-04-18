"""missing docstring"""

import numpy              as np
import pandas             as pd
from   PIL                import Image
from   skimage.filters    import threshold_otsu
# from   skimage.io         import imread
from   skimage.morphology import binary_closing, remove_small_objects
from   skimage.measure    import label, regionprops
from   skimage.util       import img_as_ubyte, img_as_bool


def region_filter(region):
    """missing docstring"""
    # main concern here is that the key regions are included
    # those are usually rectangular
    # therefore extent is the most reliable metric to filter by
    return region.extent <= 0.8


def filter_regions_by_props(regions):
    """missing docstring"""
    return list(filter(region_filter, regions))


def original_to_segmented(image_path):
    """missing docstring"""

    # reading data
    greyscale_img = Image.open(image_path).convert("L")
    greyscale_array = np.array(greyscale_img)
    
    # cropping out the interesting part and just using green channel
    greyscale_cropped_image = greyscale_array[:600, :600]

    # segmenting
    global_threshold = threshold_otsu(greyscale_cropped_image)

    # filling holes
    greyscale_closed = binary_closing(np.invert(greyscale_cropped_image > global_threshold))

    # removing small objects outside of leaf
    greyscale_closed_rem = remove_small_objects(greyscale_closed, min_size=128, connectivity=2)

    return img_as_ubyte(greyscale_closed_rem)


def segmented_to_labelled(img):
    """missing docstring"""
    return label(img_as_bool(img))


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
