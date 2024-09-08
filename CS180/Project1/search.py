import numpy as np
import skimage as sk
import skimage.io as skio
import math
import utils


def search(image1, image2, sc = 10, basic_x = 0, basic_y = 0):
    x_1 = image1.shape[0]
    x_2 = image2.shape[0]

    y_1 = image1.shape[1]
    y_2 = image2.shape[1]
    
    x_p = 0
    y_p = 0
    maxx = -999999

    for i_ in range(-sc, sc):
        for j_ in range(-sc, sc):
            i = basic_x + i_
            j = basic_y + j_
           # print('search')
           # print([i, j])
            # dist =  utils.Eu_dis_div(image1, image2, i, j)

            a = np.roll(image2, i, axis=0)
            a = np.roll(a, j ,axis = 1)
            
            # x_max = max([0,i])
            # x_min = min([0,i])

            # y_max = max([0,j])
            # y_min = min([0,j])

            # a2 = image2[x_max - i : x_min - i + x_2, y_max - j : y_min - j + y_2]
            # a1 = image1[x_max : x_min + x_1, y_max : y_min + y_1]

            # if i >= 0:
            #     if j >= 0:
            #         dist =  utils.normalized_cross_correlation(image1[i:x_1, j:y_1], image2[0 : x_2 - i,0 : y_2 - j])
            #     else:
            #         dist =  utils.normalized_cross_correlation(image1[i:x_1, 0 : y_1 + j], image2[0 : x_2-i,  -j : y_2])
            # else:
            #     if j >= 0:
            #         dist =  utils.normalized_cross_correlation(image1[0 : x_1 + i, j:y_1], image2[-i:, 0:y_2 - j])
            #     else:
            #         dist =  utils.normalized_cross_correlation(image1[0 : x_1 + i, 0 : y_1 + j], image2[-i:, -j: y_2])

            dist = utils.normalized_cross_correlation(image1, a)
            
            # dist = abs(dist)

            if maxx <= dist:
                maxx = dist
                x_p = i
                y_p = j

    return x_p, y_p

def shift_and_compute_ncc(base_img, search_img, max_shift, base_offset=(0, 0)):
    h_base, w_base = base_img.shape[:2]
    h_search, w_search = search_img.shape[:2]

    best_ncc = -1
    best_shift = (0, 0)

    base_dx, base_dy = base_offset  
    for dy in range(base_dy - max_shift, base_dy + max_shift + 1):
        for dx in range(base_dx - max_shift, base_dx + max_shift + 1):

            y_start_base = max(0, dy)
            y_start_search = max(0, -dy)
            y_end_base = min(h_base, h_base + dy)
            y_end_search = min(h_search, h_search + dy)

            x_start_base = max(0, dx)
            x_start_search = max(0, -dx)
            x_end_base = min(w_base, w_base + dx)
            x_end_search = min(w_search, w_search + dx)

            base_patch = base_img[y_start_base:y_end_base, x_start_base:x_end_base]
            search_patch = search_img[y_start_search:y_end_search, x_start_search:x_end_search]

            if base_patch.size == 0 or search_patch.size == 0:
                continue


            ncc = utils.calculate_ncc(base_patch, search_patch)

            if ncc > best_ncc:
                best_ncc = ncc
                best_shift = (dx, dy)

    return best_shift[0], best_shift[1]