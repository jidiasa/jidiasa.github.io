# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio
import utils
from search import search
from image_py_Gaussian import impyramid

# name of the input file
path = 'D:/JackyWang/college/Berkeley/CS180/data/data'
imname = '/self_portrait.tif'

# read in the image
im = skio.imread(path + imname)

# convert to double (might want to do this later on to save memory)    
im = sk.img_as_float(im)
    
# compute the height of each part (just 1/3 of total)
height = np.floor(im.shape[0] / 3.0).astype(int)
print('image shape:')

print(im.shape)

# separate color channels
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]

# images = [b, g, r]

# cropped_images = utils.crop_images_to_common_area(images)

# b = cropped_images[0]
# g = cropped_images[1]
# r = cropped_images[2]

print(b.shape)

x_g, y_g = impyramid(b, g)
x_r, y_r = impyramid(b, r)
# x_g, y_g = search(b, g)
# x_r, y_r = search(b, r)

# align the images
# functions that might be useful for aligning the images include:
# np.roll, np.sum, sk.transform.rescale (for multiscale)

### ag = align(g, b)

print('x_g ' + str(x_g))
print('x_r ' + str(x_r))
print('y_g ' + str(y_g))
print('y_r ' + str(y_r))




# ar = np.roll(r, x_r, axis = 1)
# ar = np.roll(ar, y_r, axis = 0)

# ag = np.roll(g, x_g, axis = 1)
# ag = np.roll(ag, y_g, axis = 0)

ar = r
ag = g

### ar = align(r, b)

size = b.shape

x_max = max([x_r, 0, x_g])
x_min = min([x_r, 0, x_g])

y_max = max([y_r, 0, y_g])
y_min = min([y_r, 0, y_g])

ar = ar[x_max - x_r : x_min - x_r + size[0], y_max - y_r : y_min - y_r + size[1]]
ag = ag[x_max - x_g : x_min - x_g + size[0], y_max - y_r : y_min - y_r + size[1]]
b = b[x_max : x_min + size[0], y_max : y_min + size[1]]


# create a color image
im_out = np.dstack((ar, ag, b))

# save the image
im_out = (im_out * 255).astype(np.uint8)
fname = '/out/out_fname.jpg'
skio.imsave(path + fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()