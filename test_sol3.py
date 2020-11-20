import unittest

import sol3 as sol
from imageio import imread
from skimage.color import rgb2gray
import numpy as np
from sympy.ntheory import binomial_coefficients_list
import os
import inspect
import runner as run
import ast

import cv2
from scipy.stats import pearsonr

import matplotlib.pyplot as plt


# ================================ helper functions ================================


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


def _mse(im1, im2):
    """
    Calculates 'Mean Squared Error' between the two similar shaped images, which is the sum of the squared difference
    between the two images. Normalizes the MSE.
    The lower the error the more similar the images are.
    :param im1: First image.
    :param im2: Second image.
    :return: err: The error.
    """
    err = np.sum((im1.astype("float") - im2.astype("float")) ** 2)
    err /= float(im1.shape[0] * im1.shape[1])

    return err


def _generate_images(directory_path):
    """
    Generates a list of images from a list of image names.
    :param names: List of strings.
    :return: A list of grayscale images.
    """
    directory = os.path.abspath(directory_path)
    images = [(read_image(os.path.join(directory, filename), 1), filename) for filename in os.listdir(directory) if
              filename.endswith('.jpg')]
    return images


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


# -------------------------------- ex3-specifics --------------------------------


def _cv2_build_gaussian_pyramid(im, levels):
    """
    Builds a gaussian pyramid for a given image using the built in reduce function in cv2.
    :param im: The given image.
    :param levels: Amount of levels for the pyramid.
    :return: gaussian_pyr: The gaussian pyramid.
    """
    layer = im.copy()
    # Building a gaussian pyramid using a cv2 builtIn capabilities
    gaussian_pyr = []
    gaussian_pyr.append(np.array(im))
    for i in range(levels - 1):
        layer = np.array(cv2.pyrDown(layer))
        gaussian_pyr.append(layer)
    return gaussian_pyr


def _cv2_build_laplacian_pyramid(gaussian_pyr):
    """
    Builds a laplacian pyramid from a given gaussian pyramid using cv2 built in expand.
    :param gaussian_pyr: The given gaussian pyramid.
    :return: The laplacian pyramid.
    """
    # Computing a laplacian pyramid using the gaussian pyramid created using cv2
    laplacian_pyr = []
    laplacian_pyr.append(gaussian_pyr[-1])
    for i in range(len(gaussian_pyr) - 1, 0, -1):
        size = (gaussian_pyr[i - 1].shape[1], gaussian_pyr[i - 1].shape[0])
        gaussian_expanded = cv2.pyrUp(gaussian_pyr[i], dstsize=size)
        laplacian_layer = cv2.subtract(gaussian_pyr[i - 1], gaussian_expanded)
        laplacian_pyr.append(laplacian_layer)
    laplacian_pyr = laplacian_pyr[::-1]
    return laplacian_pyr


# ================================ unittest class ================================


class TestEx3(unittest.TestCase):
    """
    The unittest testing suite.
    """

    # ================================ setup/teardown functions ================================

    @classmethod
    def setUpClass(cls):
        """
        Generates all necessary data for tests, runs before all other tests.
        :return: -
        """
        cls.images = _generate_images(r'external')
        cls.filter_sizes = [3, 5, 7, 9]

    # ================================ general helpers ================================

    def _structure_tester(self, func, signature, no_loops, no_return):
        """
        Checks a given function's structure is correct according to the pdf.
        :param func: The given function.
        :param signature: Expected signature.
        :param no_loops: True if there should be no loops.
        :param no_return: True if the function returns nothing.
        :return: -
        """
        func_name = str(func.__name__)

        # Check no loops were used in implementation if needed
        if no_loops:
            self.assertEqual(False, _uses_loop(func),
                             msg=f"Your {func_name} implementation should not contain loops")

        # Check there is no return statement if needed
        if no_return:
            self.assertEqual(False, _has_return(func),
                             msg=f"Your {func_name} implementation should not have a return statement")

        # Checks the signature of the function equals the pdf
        self.assertEqual(signature, str(inspect.signature(func)),
                         msg=f"{func_name} signature should be {signature} but is {str(inspect.signature(func))}")

    def _compare_images(self, expected_im, sol_image, tested_im_name, tested_func_name, pearson_thresh=0.9,
                        mse_thresh=0.05):
        """
        Compares two images by first comparing their shape, and then checking their similarities by checking the pearson's
        "r" coefficient is higher than "pearson_tresh" and the mse error is lower than "mse_tresh".
        :param expected_im: The reference image.
        :param sol_image: The tested image.
        :param tested_im_name: Name of the image being tested.
        :param tested_func_name: Name of the function that changed the image.
        :param pearson_thresh: The pearson's r coefficient threshold.
        :param mse_thresh: The mse error threshold.
        :return:
        """
        self.assertEqual(expected_im.shape, sol_image.shape,
                         msg=f"The '{tested_func_name}' function on the {tested_im_name} image should be similar to the built in output, so the output's shape should be equal to the shape of the built in shape")
        r = pearsonr(expected_im.flatten(), sol_image.flatten())[0]
        # print(f"for {tested_im_name}, the pearsonr was {co}")
        #
        # print(f"for {tested_im_name}, mse was : {self.mse(im1, im2)}")
        #
        # print(f"\n================\n")
        self.assertTrue(r > pearson_thresh and _mse(expected_im, sol_image) < mse_thresh,
                        msg=f"The {tested_im_name} image from {tested_func_name}'s output is not so similar to the built in implementation... maybe you should used plt.imshow on the new image and see what it looks like")

    # ================================ Part III Tests ================================

    # -------------------------------- 3.1 test module --------------------------------

    def _init_pyr_module_variables(self, filter_size, func, max_levels, orig_matrix, test_name):
        """
        Initiates all of the needed values for the pyramid testing module.
        :param filter_size: The size of the asked filter.
        :param func: The function to test.
        :param max_levels: The given max_levels parameter.
        :param orig_matrix: The matrix/image to test on.
        :param test_name: Name of the matrix/image.
        :return: A list of all needed values:
                1. :max_val: The maximum value in the original array.
                2. :name: The function's name.
                3. :orig_shape: The shape of the original matrix/image.
                4. :output: The output of applying the function to the supplied inputs.
                5. :test_name: Info about the matrix/image that is being tested.
                6. :true_binom: The expected filter array.
        """
        name = func.__name__
        output = func(orig_matrix, max_levels, filter_size)
        true_binom = np.array(binomial_coefficients_list(filter_size - 1))
        true_binom = (true_binom / np.sum(true_binom)).reshape(1, true_binom.shape[0])
        orig_shape = orig_matrix.shape
        max_val = np.max(orig_matrix)
        test_name = f"(test on : {test_name}, max_levels: {max_levels}, filter_size: {filter_size})"
        return max_val, name, orig_shape, output, test_name, true_binom

    def _check_pyr_structure(self, max_val, name, orig_shape, pyr, test_name, max_levels):
        """
        Tests the internal structure of the pyramid (Tests shapes of levels, min level size and sometimes (gaussian)
        tests normalization of values.
        :param max_val: The maximum value in the original array.
        :param name: The function's name.
        :param orig_shape: The shape of the original matrix/image.
        :param pyr: The outputted pyramid.
        :param test_name: Info about the matrix/image that is being tested.
        :return: -
        """
        # Checks maximal pyramid size
        self.assertTrue(max_levels >= len(pyr),
                        msg=f'pyr size should not exceed "max_levels" in {name} function on {test_name}')

        # Checks minimal level size
        last_lvl_shape = np.array(pyr[-1]).shape
        self.assertTrue(last_lvl_shape[0] >= 16 and last_lvl_shape[1] >= 16,
                        msg=f"In {name}, shape of pyr's last level should not be smaller than (16,16)")

        # Checks internal shapes and vals
        # TODO: Check that the dimensions are definitely going to be powers of 2
        cur_row_amount, cur_col_amount = orig_shape
        for i, level in enumerate(pyr):
            self.assertEqual(f"{cur_row_amount, cur_col_amount}", str(np.array(level).shape),
                             msg=f"level {i} in pyr created by {name} on the matrix named '{test_name}' should be of size ({cur_row_amount, cur_col_amount})")
            cur_row_amount = np.int(cur_row_amount / 2)
            cur_col_amount = np.int(cur_col_amount / 2)

            if name == "build_gussian_pyramid":
                self.assertTrue((0 <= np.min(level) and np.max(level) <= max_val),
                                msg=f"Values of pyr levels in {name}'s output should not be higher than the original image's max value, maybe you forgot to normalize the filter_vec?\nmin_val:{np.min(level)}, max_val:{np.max(level)},level:{i},test_name:{test_name}")

    def _test_pyr_module(self, func, orig_matrix, test_name, max_levels, filter_size):
        """
        A module that tests the implementation of a pyramid creating function on a specific matrix/image.
        :param func: The function to test.
        :param orig_matrix: The matrix/image to test on.
        :param test_name: Info about the matrix/image that is being tested.
        :param max_levels: The given max_levels parameter.
        :param filter_size: The given filter_size parameter.
        :return: -
        """

        # Init variables
        max_val, name, orig_shape, output, test_name, true_binom = self._init_pyr_module_variables(filter_size, func,
                                                                                                   max_levels,
                                                                                                   orig_matrix,
                                                                                                   test_name)

        # get output vals
        pyr, filter_vec = output

        # Checks output shape
        self.assertEqual(2, len(output), msg=f'{name} should return an array of length 2')

        # Checks pyr is a normal python array (list)
        self.assertEqual(type([]), type(pyr), msg=f'In {name}, pyr type should be a normal python array (list)')

        # Checks filter_vec is correct
        self.assertEqual(f"(1, {filter_size})", str(filter_vec.shape),
                         msg=f"filter_vec's shape should be (1, {filter_size}), but is {filter_vec.shape}")
        self.assertIsNone(np.testing.assert_array_equal(true_binom, filter_vec,
                                                        err_msg=f"\nERROR WAS:\nfilter_vec should look like {true_binom}, but looks like {filter_vec}\n"))

        # Checks pyr's dimensions
        self._check_pyr_structure(max_val, name, orig_shape, pyr, test_name, max_levels)

    # -------------------------------- 3.1 helpers --------------------------------

    def _test_pyr_static(self, func):
        """
        Runs multiple static tests on the images in the "externals" folder.
        :param func: The function to test.
        :return: -
        """

        # Test 'test_gaussian_pyr' structure
        self._structure_tester(func, r'(im, max_levels, filter_size)', False, False)

        # Basic images test, fixed filter size and fixed default max_levels from pdf
        for img in self.images:
            self._test_pyr_module(func, img[0], img[1],
                                  np.int(np.log(np.array(img[0]).shape[0]) - 1), 3)

    def _test_pyr_random(self, func):
        """
        Runs multiple RANDOM tests on a pyramid constructing function.
        Checks implementation over the test images with random "max_levels" and "filter_size" variables.
        Checks implementation over stress tests (45 random matrices of varied sizes and random arguments).
        :param func: The function to test.
        :return: -
        """

        # Basic images, random max level and random filter size
        for img in self.images:
            self._test_pyr_module(func, img[0], img[1],
                                  np.random.choice(np.arange(1, np.int(np.log(np.array(img[0]).shape[0]) - 1))),
                                  np.random.choice(self.filter_sizes))

        # Random stress test
        for i in range(8):
            length = 2 ** (i + 7)
            for j in range(9 - i):
                orig_matrix = np.random.randint(255, size=(length, length))
                self._test_pyr_module(func, orig_matrix, f"random(0,255)_sizeof_({length}, {length})",
                                      i + 6, np.random.choice(self.filter_sizes))

    # -------------------------------- 3.1 tests --------------------------------

    def test_build_gaussian_pyramid_static(self):
        """
        Runs a static test on "build_gaussian_pyramid".
        :return: -
        """
        self._test_pyr_static(sol.build_gaussian_pyramid)

    def test_build_gaussian_pyramid_random(self):
        """
        Runs a random test on "build_gaussian_pyramid".
        :return: -
        """
        self._test_pyr_random(sol.build_gaussian_pyramid)

    def test_build_laplacian_pyramid_static(self):
        """
        Runs a static test on "build_laplacian_pyramid".
        :return: -
        """
        self._test_pyr_static(sol.build_laplacian_pyramid)

    def test_build_laplacian_pyramid_random(self):
        """
        Runs a random test on "build_laplacian_pyramid".
        :return: -
        """
        self._test_pyr_random(sol.build_laplacian_pyramid)

    # -------------------------------- 3.2 test module --------------------------------

    def _test_reconstruct_module(self, im, im_name):
        """
        Tests module for laplacian_to_image on a specific image.
        :param im: The image to test.
        :param im_name: The image's name.
        :return: -
        """

        my_gaussian, filter_vec = sol.build_gaussian_pyramid(im, 4, 5)
        my_laplacian, filter_vec = sol.build_laplacian_pyramid(im, 4, 5)

        gaussian_pyr = _cv2_build_gaussian_pyramid(im, 4)
        laplacian_pyr = _cv2_build_laplacian_pyramid(gaussian_pyr)

        new_im = sol.laplacian_to_image(laplacian_pyr, filter_vec, np.ones(len(laplacian_pyr)))

        self._compare_images(im, new_im, im_name, r'laplacian_to_image')

    # -------------------------------- 3.2 test --------------------------------

    def test_laplacian_to_image(self):
        """
        Tests laplacian_to_image. I test it on a built in implementation laplacian pyramid so that it isn't dependant
        on the user's implementation of other functions.
        :return: -
        """
        # Tests function structure according to pdf
        self._structure_tester(sol.laplacian_to_image, r'(lpyr, filter_vec, coeff)', False, False)

        # Uses a laplacian pyramid created using cv2 and compares laplacian_to_image's output on it to the original
        # image.
        for test_im in self.images:
            self._test_reconstruct_module(test_im[0], test_im[1])

    # -------------------------------- 3.3 test module --------------------------------

    def _test_reder_module(self, im, im_name, level, is_lap):
        """
        Tests the render_pyramid function on a single image.
        :param im: A grayscale image to test on.
        :param im_name: Name of the image.
        :param level: Amount of levels for the pyramid.
        :return: -
        """

        # Computes the gaussian/laplacian pyramid using the cv2 implementations
        pyr = _cv2_build_gaussian_pyramid(im, level)
        if is_lap:
            pyr = _cv2_build_laplacian_pyramid(pyr)

        # computes the render using the solution
        res = sol.render_pyramid(pyr, level)

        # computes the expected x_axis shape of the output (cols)
        x_size = im.shape[1]
        factor = 2
        x_size = x_size
        for i in range(1, level):
            x_size += (im.shape[1] // (factor ** i))

        # Compares the expected result shape to the actual shape
        self.assertEqual(x_size, res.shape[1],
                         msg=f"After rendering, the image's ({im_name}) x axis should be of length {x_size}, but is {res.shape[1]}, tested with {level} levels")
        self.assertEqual(im.shape[0], res.shape[0],
                         msg=f"After rendering, the image's ({im_name}) y axis should be of length {im.shape[0]}, but is {res.shape[0]}, tested with {level} levels")

        # Checks the result was padded with zeros using a mask
        col = im.shape[1]
        mask = np.zeros((im.shape[0], x_size))
        for i in range(1, level):
            row = pyr[i].shape[0]
            mask[row:, col:] = 1
            col += pyr[i].shape[1]
        self.assertTrue((res*mask == 0).all(), msg=f"The blank spaces in the rendered image should be black")

    # -------------------------------- 3.3 tests --------------------------------

    def test_render_pyramid_static(self):
        """
        Tests the render_pyramid with static variables on all stock images.
        :return: -
        """

        # tests the implementation structure according to pdf
        self._structure_tester(sol.render_pyramid, r'(pyr, levels)', no_loops=False, no_return=False)

        # Checks on all stock memes (images)
        for test_im in self.images:
            self._test_reder_module(test_im[0], test_im[1], 4, is_lap=False)
            self._test_reder_module(test_im[0], test_im[1], 4, is_lap=True)

    def test_render_pyramid_random(self):
        """
        Tests 'render_pyramid' with random level variables on ALL stock images.
        :return: -
        """
        # Checks on all stock memes (images) with random pyramid level amounts
        for test_im in self.images:
            for i in range(20):
                levels = np.random.choice(np.arange(1, np.int(np.log(np.array(test_im[0]).shape[0]) - 1)))
                self._test_reder_module(test_im[0], test_im[1], levels, is_lap=False)
                self._test_reder_module(test_im[0], test_im[1], levels, is_lap=True)


if __name__ == '__main__':
    runner = run.CustomTextTestRunner()
    unittest.main(testRunner=runner)
