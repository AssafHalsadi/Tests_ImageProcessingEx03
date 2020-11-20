import cv2
from imageio import imread
from skimage.color import rgb2gray
import numpy as np
import sol3 as sol

def read_image(filename, representation):
    """
    Receives an image file and converts it into one of two given representations.
    :param filename: The file name of an image on disk (could be grayscale or RGB).
    :param representation: representation code, either 1 or 2 defining wether the output
    should be a grayscale image (1) or an RGB image (2). If the input image is grayscale,
    we won't call it with representation = 2.
    :return: An image, represented by a matrix of type (np.float64) with intensities
    normalized to the range [0,1].
    """
    assert representation in [1, 2]

    # reads the image
    im = imread(filename)
    if representation == 1:  # If the user specified they need grayscale image,
        if len(im.shape) == 3:  # AND the image is not grayscale yet
            im = rgb2gray(im)  # convert to grayscale (**Assuming its RGB and not a different format**)

    im_float = im.astype(np.float64)  # Convert the image type to one we can work with.

    if im_float.max() > 1:  # If image values are out of bound, normalize them.
        im_float = im_float / 255

    return im_float


def _show_pyramid(pyr):
    # Code that shows the pyramid
    for i in range(4):
        cv2.imshow(f"level {i} of the pyramid", pyr[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _show_gaussian_pyr(img, max_levels, filter_size):
    _show_pyramid(sol.build_gaussian_pyramid(img, max_levels, filter_size))


def _show_laplacian_pyr(img, max_levels, filter_size):
    _show_pyramid(sol.build_laplacian_pyramid(img, max_levels, filter_size))


if __name__ == '__main__':
    im = read_image(r'[YOUR IMAGE PATH HERE]', 1)
    max_levels = 4  # Enter desired levels here
    filter_size = 3  # Enter desired filter size here

    # If you want to show the gaussian pyramid of the image, uncomment this:
    # _show_gaussian_pyr(im, max_levels, filter_size)

    # If you want to show the gaussian pyramid of the image, uncomment this:
    # _show_laplacian_pyr(im, max_levels, filter_size)
