"""missing docstring"""

import numpy              as np
import pandas             as pd
# from   PIL                import Image
from   skimage.filters    import threshold_otsu
from   skimage.io         import imread#, imsave
from   skimage.morphology import binary_closing, remove_small_objects
from   skimage.measure    import label, regionprops
from   skimage.color      import label2rgb
from   skimage.util       import img_as_ubyte#, img_as_bool
# from   skimage.transform  import rescale


def filter_regions_by_extent(regions):
    """missing docstring"""
    return list(filter(lambda r: r.extent <= 0.8, regions))


def processing_pipe(image_path):
    """missing docstring"""

    # reading data, converting to greyscale, converting to numpy array
    img = imread(image_path)
    greyscale_array = np.array(img)
    
    # cropping out the interesting part & extracting green channel (rgb -> grey)
    greyscale_cropped_image = greyscale_array[:600, :600, 1]# [:600, :600, 1]

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
    images = { "original_img": img,
               "greyscale_img": greyscale_cropped_image,
               "segmented_ubyte_img_bw": img_as_ubyte(greyscale_closed_rem),
               "labelled_image": labelled_image,
               "labelled_ubyte_img_rbg": img_as_ubyte(image_label_overlay) }

    return images


def get_regions_props(img):
    """missing docstring"""
    # getting region's properties and filtering by extent
    regions_properties = regionprops(img, cache=True)
    filtered_regions = filter_regions_by_extent(regions_properties)

    # creating dataframe
    dataframe = pd.DataFrame(columns=["eccentricity", "extent", "solidity", "roundness"])

    # if len(filtered_regions) == 1:
    # getting the props for the only region
    props = filtered_regions[0]

    # manually calculating roundness
    roundness = 4 * np.pi * props.area / props.perimeter**2

    # appending data to dataframe
    dataframe.loc[len(dataframe)+1] = [props.eccentricity, props.extent, props.solidity, roundness]
    print(dataframe)
    # else:
        # print("More than 1 region remaining!")

    return dataframe
