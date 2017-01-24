
# coding: utf-8

# In[ ]:

import skimage.io as io
from skimage.color import rgb2gray
from glob import glob
import numpy as np


get_ipython().magic('matplotlib inline')


# In[ ]:

files = glob("./leafsnap-dataset/dataset/images/lab/zelkova_serrata/*.jpg")

for f in files:
    im = io.imread(f)
    # io.imsave(f[:-4] + ".bmp", im)


# In[ ]:

im1 = io.imread(files[0])
io.imshow(im1)


# In[ ]:

im1_gray = rgb2gray(im1)
io.imshow(im1_gray)


# In[ ]:



