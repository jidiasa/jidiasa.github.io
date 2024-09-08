import numpy as np
import skimage as sk
import skimage.io as skio
import utils
from search import search, shift_and_compute_ncc

def impyramid(image1, image2, factor=2, sigma=1):

    output_shape = np.array([image1.shape])
    k = np.array([1])
    dis_x = 0
    dis_y = 0

    blurred_image1 = [image1]
    blurred_image2 = [image2]

    resized_image1 = [image1]
    resized_image2 = [image2]

    while min(output_shape[-1]) > 128:
        new_shape = [x // factor for x in output_shape[-1]]
        output_shape = np.vstack((output_shape, new_shape))
        k = np.append(k, k[-1] * factor)

        blurred_image1.append(sk.filters.gaussian(resized_image1[-1], sigma=sigma))
        resized_image1.append(sk.transform.resize(blurred_image1[-1], output_shape[-1], anti_aliasing=True))
        # skio.imshow(resized_image1[-1])
        # skio.show()

        blurred_image2.append(sk.filters.gaussian(resized_image2[-1], sigma=sigma))
        resized_image2.append(sk.transform.resize(blurred_image2[-1], output_shape[-1], anti_aliasing=True))

        # skio.imshow(resized_image2[-1])
        # skio.show()
    
    level = k.shape[0]

    for i in range(level-1, -1, -1):

        dis_x = dis_x * factor
        dis_y = dis_y * factor

        # skio.imshow(resized_image2[i])
        # skio.show()

        x, y = search(resized_image1[i], resized_image2[i], 2 ** (level - i - 1), dis_x, dis_y)
        print(i,x,y)

        # for j in range(i, -1, -1):
        #     resized_image2[j] = np.roll(resized_image2[j], pow(factor, i - j) * x, axis = 1)
        #     resized_image2[j] = np.roll(resized_image2[j], pow(factor, i - j) * y, axis = 0)

        dis_x = x
        dis_y = y

        # if i == 0:
        #     # 进一步细化调整
        #     x_fine, y_fine = search(resized_image1[i], resized_image2[i], 10, dis_x, dis_y)
        #     dis_x = x_fine
        #     dis_y = y_fine


    return dis_x, dis_y
        