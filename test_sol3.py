import unittest

import sol2 as sol
from imageio import imread
from skimage.color import rgb2gray
import numpy as np
from scipy.io import wavfile
import os
import inspect
import ast


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


def _generate_images(names):
    """
    Generates a list of images from a list of image names.
    :param names: List of strings.
    :return: A list of grayscale images.
    """
    images = []
    for name in names:
        images.append((read_image(os.path.join(os.path.abspath(r'external'), f"{name}.jpg"), 1), name))
    return images


pdf_ratio = 1.25
smallest_ratio = 0.26
largest_ratio = 3.9
double_ratio = 2
half_ratio = 0.5
same = 1
ratios = [pdf_ratio, smallest_ratio, largest_ratio, double_ratio, half_ratio, same]

arr_pdf = (np.arange(1000), "arr_pdf")
arr_large_zeros = (np.zeros_like(arr_pdf), "arr_large_zeros")
arr_large_ones = (np.ones_like(arr_pdf), "arr_large_ones")
arr_normal = (np.array([1, 2, 3]), "arr_normal")
arr_same_val = (np.array([1, 1, 1]), "arr_same_val")
arr_zero_vals = (np.array([0, 0, 0]), "arr_zero_vals")
arr_single_cell = (np.array([1]), "arr_single_cell")
arr_single_zero = (np.array([0]), "arr_single_zero")
arr_empty = (np.array([]), "arr_empty")

test_arrs = [arr_pdf, arr_normal, arr_same_val, arr_zero_vals, arr_single_cell, arr_single_zero, arr_empty,
             arr_large_ones, arr_large_zeros]


# ================================ helper functions ================================


def _does_contain(function, statements):
    """
    Checks if a function implementation contains any usage of given tokens.
    :param function: The function to check in.
    :param statements: The statement tokens to find.
    :return: True if there is an instance of the statements in the function implementation, False otherwise.
    """
    nodes = ast.walk(ast.parse(inspect.getsource(function)))
    return any(isinstance(node, statements) for node in nodes)


def _uses_loop(function):
    """
    Checks if a function uses top level loops.
    :param function: The function to check in.
    :return: True if it contains loops, False otherwise.
    """
    loop_statements = ast.For, ast.While, ast.AsyncFor
    return _does_contain(function, loop_statements)


def _has_return(function):
    """
    Checks if a function contains a return statement.
    :param function: The function to check in.
    :return: True if it contains a return statement, False otherwise.
    """
    return _does_contain(function, ast.Return)


# ================================ unittest class ================================


class TestEx3(unittest.TestCase):
    """
    The unittest testing suite.
    """
    # Path to example wav supplied by the course's staff.
    aria_path = os.path.abspath(r'external/aria_4kHz.wav')
    # Path to example jpg supplied by the course's staff.
    monkey_path = os.path.abspath(r'external/monkey.jpg')

    # ================================ setup/teardown functions ================================

    @classmethod
    def setUpClass(cls):
        """
        Generates all necessary data for tests, runs before all other tests.
        :return: -
        """
        pass

    # ================================ Part I Tests ================================




if __name__ == '__main__':
    unittest.main()
