""" This module defines the image processing pipeline as described in README.md """

import numpy              as np
import pandas             as pd
from   skimage.filters    import threshold_otsu
from   skimage.io         import imread
from   skimage.morphology import binary_closing, remove_small_objects
from   skimage.measure    import label, regionprops
from   skimage.color      import label2rgb
from   skimage.util       import img_as_ubyte

def processing_pipe(image_path):
    """ This is the actual image processing function.
        It encapsulates every processing step from reading the file,
        converting it to a numpy array, cropping, performing morphological
        operations computing all region's properties (get_regions_props())
        and returning the resulting properties as well as initial the
        initial image, the intermediate and final images. """

    # reading data, converting to greyscale, converting to numpy array
    img = imread(image_path)
    greyscale_array = np.array(img)
    
    # cropping out the interesting part & extracting green channel (rgb -> grey)
    greyscale_cropped_image = greyscale_array[:, :, 1]

    # segmenting using otsu's method
    global_threshold = threshold_otsu(greyscale_cropped_image)

    # filling small holes
    greyscale_closed = binary_closing(np.invert(greyscale_cropped_image > global_threshold))

    # removing small objects outside of leaf
    greyscale_closed_rem = remove_small_objects(greyscale_closed, min_size=128, connectivity=2)

    # label the binary image and combine with rgb representation
    labelled_image = label(greyscale_closed_rem)
    image_label_overlay = label2rgb(labelled_image, image=greyscale_cropped_image)

    # compute region's properties
    regions_properties = get_regions_props(labelled_image) 

    # returning images after converting segmented image back to 8 bit format & labelling it
    image_data = { "original_img": img,
                   "greyscale_img": greyscale_cropped_image,
                   "segmented_ubyte_img_bw": img_as_ubyte(greyscale_closed_rem),
                   "labelled_image": labelled_image,
                   "labelled_ubyte_img_rgb": img_as_ubyte(image_label_overlay),
                   "regions_properties": regions_properties }

    return image_data


def get_regions_props(img):
    """ The function computes the region's properties of a labelled image.
        It returns a pandas DataFrame with the properties eccentricity,
        extent, solidity and roundness (manually computed).
        Other properties from the regionprops function or custom ones
        could be included here as well. """

    # getting region's properties and filtering by extent
    regions_properties = regionprops(img, cache=True)

    # creating dataframe
    dataframe = pd.DataFrame(columns=["eccentricity", "extent", "solidity", "roundness"])

    # getting the props for the only region
    for props in regions_properties:
        # manually calculating roundness
        roundness = 4 * np.pi * props.area / props.perimeter**2

        # appending data to dataframe
        dataframe.loc[len(dataframe)+1] = [props.eccentricity, props.extent, props.solidity, roundness]

    return dataframe
