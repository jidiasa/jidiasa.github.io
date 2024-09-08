# Project 1 by Tianhe Wang

## Project Description

This project is Project 1 of the CS180 course. The project involves cropping, aligning, and displaying three RGB images using the following methods:

1. **Data Preprocessing:**
   - The images are imported and cropped along their height into three parts, each corresponding to one of the BGR color channels. To improve alignment accuracy, border detection and cropping are performed. Borders are identified and cropped if their color values are too white (<0.02) or too dark (>0.98), while ensuring that all three images have the same dimensions after cropping.

2. **Image Alignment:**
   - The R and G images are aligned with the B image. The distance between images is measured using the NCC (Normalized Cross-Correlation) function.
     - For `.jpg` images, a direct search method is used. A pixel-by-pixel search is performed within a displacement range of (-15, 15) until the best match is found.
     - For larger `.tif` images, a pyramid algorithm is used. Each layer of the image is blurred and sampled every factor = 2. Gaussian blur is applied, where each pixel is a weighted sum of its surrounding pixels. The process is repeated until fewer than 64 pixels remain. Then, the best match is searched from small to large layers, with displacement multiplied by the scaling factor to achieve a coarse-to-fine search.

3. **Image Composition:**
   - Based on the obtained displacements, only the overlapping regions of the three images are extracted and cropped. The resulting image is then converted into a color image with values from 0 to 255.

## Results

The results show that the images are well-aligned with minimal ghosting and proper border cropping, achieving the task objectives. Although the `.tif` images are much larger than the `.jpg` images, the pyramid algorithm significantly reduced the runtime and expanded the search range.

A drawback is that ghosting is not completely eliminated; some ghosting is still visible under magnification, indicating that the best match has not been obtained. This may be due to the NCC distance calculation method, as using `np.roll` for NCC calculation affects the result by including surrounding pixels. Additionally, NCC itself may have limitations, as it might struggle with images containing objects with contrasting colors against backgrounds. Consideration of alternative image distance matching algorithms may be needed.
