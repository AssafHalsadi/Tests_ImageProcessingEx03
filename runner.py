import unittest.runner
import itertools
import test_sol3 as tester
import re

DOGGO ="          _ _\n\
     _(,_/ \ \____________\n\
     |`. \_@_@   `.     ,'\n\
     |\ \ .        `-,-'\n\
     || |  `-.____,-'\n\
     || /  /\n\
     |/ |  |\n\
`..     /   \\\n\
  \\   /    |\n\
  ||  |      \\\n\
   \\ /-.    |\n\
   ||/  /_   |\n\
   \(_____)-'_)"

DOGGO_FRAME = ": 𝗦𝗨𝗖𝗖𝗘𝗦𝗦 𝗗𝗢𝗚𝗚𝗢 𝗪𝗜𝗦𝗛𝗘𝗦 𝗬𝗢𝗨 𝗦𝗨𝗖𝗖𝗘𝗦𝗦 :"

YOU_PASSED = " ✩ ░▒▓▆▅▃▂▁ 𝐘𝐎𝐔 𝐏𝐀𝐒𝐒𝐄𝐃 ▁▂▃▅▆▓▒░ ✩"

YOU_FAILED = "❚█══YOU FAILED══█❚"


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

    def addSuccess(self, test):
        super(CustomTextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("✔ You passed ✔")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addFailure(self, test, err):
        super(CustomTextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("❌ You failed ❌")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

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
    # tests = ['test_build_gaussian_pyramid_random', 'test_build_gaussian_pyramid_static', 'test_build_laplacian_pyramid_random', 'test_build_laplacian_pyramid_static', 'test_laplacian_to_image', 'test_render_pyramid_random', 'test_render_pyramid_static']
    # return [tester.TestEx3(method) for method in tests]
    return [tester.TestEx3(method) for method in dir(tester.TestEx3) if method.startswith('test')]


if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    tests = get_tests()

    test_suite.addTests(tests)

    runner = CustomTextTestRunner(verbosity=2).run(test_suite)
    if runner.wasSuccessful():
        print(YOU_PASSED)
        print(DOGGO_FRAME)
        print(DOGGO)
    else:
        print(YOU_FAILED)
