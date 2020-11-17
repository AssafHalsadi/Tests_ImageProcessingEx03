import unittest.runner
import itertools
import test_sol3 as tester
import re


class CustomTextTestResult(unittest.runner.TextTestResult):
    """Extension of TextTestResult to support numbering test cases"""

    def __init__(self, stream, descriptions, verbosity):
        """Initializes the test number generator, then calls super impl"""

        self.test_numbers = itertools.count(1)
        stream.write(f"================================================\n            ==== Starting Tests ====\n================================================\n")
        return super(CustomTextTestResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        """Writes the test number to the stream if showAll is set, then calls super impl"""

        if self.showAll:
            progress = f'[{next(self.test_numbers)}/{self.test_case_count}] '
            self.stream.write(progress)

            # Also store the progress in the test itself, so that if it errors,
            # it can be written to the exception information by our overridden
            # _exec_info_to_string method:
            test.progress_index = progress

        return super(CustomTextTestResult, self).startTest(test)

    def _exc_info_to_string(self, err, test):
        """Gets an exception info string from super, and prepends 'Test Number' line"""

        info = super(CustomTextTestResult, self)._exc_info_to_string(err, test)

        if self.showAll:
            info = 'Test number: {index}\n{info}'.format(
                index=test.progress_index,
                info=re.sub("AssertionError:(.*?):", "\nERROR WAS:\n", info)
            )

        return info


class CustomTextTestRunner(unittest.runner.TextTestRunner):
    """Extension of TextTestRunner to support numbering test cases"""

    resultclass = CustomTextTestResult

    def run(self, test):
        """Stores the total count of test cases, then calls super impl"""

        self.test_case_count = test.countTestCases()
        return super(CustomTextTestRunner, self).run(test)

    def _makeResult(self):
        """Creates and returns a result instance that knows the count of test cases"""

        result = super(CustomTextTestRunner, self)._makeResult()
        result.test_case_count = self.test_case_count
        return result


def get_tests():
    """
    Generates and returns a list of all the names of tests to run through the textual interface
    :return: The aforementioned list.
    """
    # tests = ['test_DFT2_IDFT2', 'test_DFT_IDFT_1D', 'test_change_rate', 'test_change_samples', 'test_resize', 'test_resize_spectrogram', 'test_resize_vocoder']
    # return [tester.TestEx2(method) for method in tests]
    return [tester.TestEx3(method) for method in dir(tester.TestEx3) if method.startswith('test_')]


if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    tests = get_tests()

    test_suite.addTests(tests)

    CustomTextTestRunner(verbosity=2).run(test_suite)