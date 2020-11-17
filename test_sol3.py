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

    # ================================ Part III Tests ================================

    # -------------------------------- 3.1 test module --------------------------------

    def _test_pyr_module(self, func, orig_matrix, test_name, max_levels, filter_size):

        name = func.__name__

        output = func(orig_matrix, max_levels, filter_size)
        true_binom = np.array(binomial_coefficients_list(filter_size - 1))
        true_binom = (true_binom / np.sum(true_binom)).reshape(1, true_binom.shape[0])
        orig_shape = orig_matrix.shape
        max_val = np.max(orig_matrix)
        test_name = f"(test on : {test_name}, max_levels: {max_levels}, filter_size: {filter_size})"

        # Checks output shape
        self.assertEqual(2, len(output), msg=f'{name} should return an array of length 2')
        pyr, filter_vec = output

        # Checks pyr is a normal python array (list)
        self.assertEqual(type([]), type(pyr), msg=f'In {name}, pyr type should be a normal python array (list)')

        # Checks pyramid size
        self.assertTrue(max_levels >= len(pyr),
                        msg=f'pyr size should not exceed "max_levels" in {name} function on {test_name}')

        # Checks filter_vec is correct
        self.assertEqual(f"(1, {filter_size})", str(filter_vec.shape),
                         msg=f"filter_vec's shape should be (1, {filter_size}), but is {filter_vec.shape}")
        self.assertIsNone(np.testing.assert_array_equal(true_binom, filter_vec,
                                                        err_msg=f"\nERROR WAS:\nfilter_vec should look like {true_binom}, but looks like {filter_vec}\n"))

        # Checks pyr's dimensions
        last_lvl_shape = np.array(pyr[-1]).shape
        self.assertTrue(last_lvl_shape[0] >= 16 and last_lvl_shape[1] >= 16,
                        msg=f"In {name}, shape of pyr's last level should not be smaller than (16,16)")

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

    # -------------------------------- 3.1 helpers --------------------------------

    def _test_pyr_static(self, func):

        # Test 'test_gaussian_pyr' structure
        self._structure_tester(func, r'(im, max_levels, filter_size)', False, False)

        # Basic images test, fixed filter size and fixed default max_levels from pdf
        for img in self.images:
            self._test_pyr_module(func, img[0], img[1],
                                  np.int(np.log(np.array(img[0]).shape[0]) - 1), 3)

    def _test_pyr_random(self, func):

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
        self._test_pyr_static(sol.build_gaussian_pyramid)

    def test_build_gaussian_pyramid_random(self):
        self._test_pyr_random(sol.build_gaussian_pyramid)

    def test_build_laplacian_pyramid_static(self):
        self._test_pyr_static(sol.build_laplacian_pyramid)

    def test_build_laplacian_pyramid_random(self):
        self._test_pyr_random(sol.build_laplacian_pyramid)


if __name__ == '__main__':
    runner = run.CustomTextTestRunner()
    unittest.main(testRunner=runner)
