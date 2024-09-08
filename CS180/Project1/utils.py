import numpy as np
import skimage as sk
import skimage.io as skio
import math

def Eu_dis_div(image1, image2, x_p, y_p):
    x_1 = image1.shape[0]
    x_2 = image2.shape[0]

    y_1 = image1.shape[1]
    y_2 = image1.shape[1]

    dist = 0.0
    num_pix = 0

    if x_p >= 0:
        if y_p >= 0:
            for i in range(x_p, x_1):
                for j in range(y_p, y_1):
                    num_pix = num_pix + 1
                    dist = dist + (image1[i][j] - image2[i - x_p][j - y_p]) * (image1[i][j] - image2[i - x_p][j - y_p])
            dist = dist / num_pix
            dist = math.sqrt(dist)
        else:
            y_p = 0 - y_p
            for i in range(x_p, x_1):
                for j in range(y_p, y_2):
                    num_pix = num_pix + 1
                    dist = dist + (image1[i][j - y_p] - image2[i - x_p][j]) * (image1[i][j - y_p] - image2[i - x_p][j])
                dist = dist / num_pix
                dist = math.sqrt(dist)
    else:
        x_p = 0 - x_p
        if y_p >= 0:
            for i in range(x_p, x_1):
                for j in range(y_p, y_1):
                    num_pix = num_pix + 1
                    dist = dist + (image1[i - x_p][j] - image2[i][j - y_p]) * (image1[i - x_p][j] - image2[i][j - y_p])
            dist = dist / num_pix
            dist = math.sqrt(dist)
        else:
            y_p = 0 - y_p
            for i in range(x_p, x_1):
                for j in range(y_p, y_2):
                    num_pix = num_pix + 1
                    dist = dist + (image1[i - x_p][j - y_p] - image2[i][j]) * (image1[i - x_p][j - y_p] - image2[i][j])
                dist = dist / num_pix
                dist = math.sqrt(dist)

    return dist

def normalized_cross_correlation(img1, img2):

    mean1 = np.mean(img1)
    mean2 = np.mean(img2)

    numerator = np.sum((img1 - mean1) * (img2 - mean2))
    denominator = np.sqrt(np.sum((img1 - mean1) ** 2) * np.sum((img2 - mean2) ** 2))
    
    if denominator == 0:
        return 0

    return numerator / denominator

# def trim_borders(image, threshold=0.02):
#     if len(image.shape) == 3:
#         image_gray = np.mean(image, axis=2).astype(np.uint8)
#     else:
#         image_gray = image

#     mask = image_gray > threshold  

#     coords = np.argwhere(mask)
#     y_min, x_min = coords.min(axis=0)
#     y_max, x_max = coords.max(axis=0)

#     cropped_image = image[y_min:y_max+1, x_min:x_max+1]

#     return cropped_image

def find_common_crop_area(images, lower_thresh=0.02, upper_thresh=0.98):
    y_min_common, x_min_common = None, None
    y_max_common, x_max_common = None, None

    for image in images:

        image_gray = image
        
        mask = (image_gray > lower_thresh) & (image_gray < upper_thresh)

        coords = np.argwhere(mask)
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)

        if y_min_common is None:
            y_min_common, x_min_common = y_min, x_min
            y_max_common, x_max_common = y_max, x_max
        else:
            y_min_common = max(y_min_common, y_min)
            x_min_common = max(x_min_common, x_min)
            y_max_common = min(y_max_common, y_max)
            x_max_common = min(x_max_common, x_max)

    return y_min_common, y_max_common, x_min_common, x_max_common

def crop_images_to_common_area(images, lower_thresh=0.02, upper_thresh=0.98):
    y_min, y_max, x_min, x_max = find_common_crop_area(images, lower_thresh, upper_thresh)

    cropped_images = [image[y_min:y_max+1, x_min:x_max+1] for image in images]

    return cropped_images

def calculate_ncc(img1, img2):
    img1 = img1 - np.mean(img1)  
    img2 = img2 - np.mean(img2) 

    numerator = np.sum(img1 * img2)
    denominator = np.sqrt(np.sum(img1 ** 2) * np.sum(img2 ** 2))

    if denominator == 0:
        return 0
    else:
        return numerator / denominator