
# coding: utf-8


get_ipython().magic('matplotlib inline')
import skimage.io as io
from skimage.color import rgb2gray
from glob import glob
import numpy as np
from skimage.filter import threshold_otsu
from skimage import img_as_uint
from skimage.morphology import closing
from skimage.morphology import square
from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects
from skimage.color import label2rgb

files = glob("./leafsnap-dataset/dataset/images/lab/zelkova_serrata/*.jpg")

for f in files[:10]:
    # reading data
    im = io.imread(f)
    
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
    image_label_overlay = label2rgb(labelled, image=bw_closed_rem)
    
    properties = regionprops(labelled)
    
    
    # saving
    io.imsave(f[:-4] + ".bmp", img_as_uint(bw_closed_rem))
    io.imsave(f[:-4] + "_label.bmp", image_label_overlay)

