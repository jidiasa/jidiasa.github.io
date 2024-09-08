import numpy as np
import skimage as sk
import skimage.io as skio
import utils
from image_py_Gaussian import impyramid
from search import search
from pathlib import Path
import os

path = 'D:/JackyWang/college/Berkeley/CS180/data/data'

def list_and_load_jpg_images(folder_path):
    
    folder = Path(folder_path)
    images = []
    filenames = []
    num = 0

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(".tif"):
            file_path = os.path.join(folder_path, filename)
            image = skio.imread(file_path)
            images.append(image)
            filenames.append(filename)
            num = num + 1
    
    return images, filenames, num

folder_path = 'D:/JackyWang/college/Berkeley/CS180/data/data'
images, jpg_filenames, num = list_and_load_jpg_images(folder_path)
print(num)

for i in range(0, num):
    im = images[i]
    im = sk.img_as_float(im)
    
    height = np.floor(im.shape[0] / 3.0).astype(int)
    print(height)
    print(im.shape)

    # separate color channels
    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    # imagess = [b, g, r]

    # cropped_images = utils.crop_images_to_common_area(imagess)

    # b = cropped_images[0]
    # g = cropped_images[1]
    # r = cropped_images[2]

    # x_g, y_g = search(b, g)
    # x_r, y_r = search(b, r)
    x_g, y_g = impyramid(b, g)
    x_r, y_r = impyramid(b, r)
    # align the images
    # functions that might be useful for aligning the images include:
    # np.roll, np.sum, sk.transform.rescale (for multiscale)

    ### ag = align(g, b)

    print(x_g)
    print(x_r)

    # ag = np.roll(g, x_g, axis = 1)
    # ag = np.roll(ag, y_g, axis = 0)

    # ar = np.roll(r, x_r, axis = 1)
    # ar = np.roll(ar, y_r, axis = 0)
    ar = r
    ag = g
    ### ar = align(r, b)

    print(ar.shape)

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
    print(im_out.shape)

    # save the image
    im_out = (im_out * 255).astype(np.uint8)
    fname = '/out/out3_' + jpg_filenames[i]
    skio.imsave(path + fname, im_out)

