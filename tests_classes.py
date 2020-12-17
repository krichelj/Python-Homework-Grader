import sys
import os
import re
import difflib
import importlib
import collections
import numpy as np
import time

WRONG_CLASS_DEDUCTION = 0.5

class ListStream:
    """this class enables to save as a string everything that was printed"""

    def __init__(self):
        self.data = ''

    def write(self, s):
        self.data = self.data + s

    def flush(self):
        pass


def compare_strings(out_str, expected_str, difference_num=10):
    """checks if two strings are somewhat similar"""

    if out_str == expected_str:
        return True
    elif out_str == '' and expected_str != '':
        return False
    elif out_str != '' and expected_str == '':
        return False
    elif out_str[-1] == " " and expected_str[-1] != " ":
        out_str = out_str[:-1]
    output_list = [li for li in difflib.ndiff(out_str, expected_str) if li[0] != ' ']

    if len(output_list) < difference_num:
        return True
    return False


class Test:
    def __init__(self, test_phrase: str, points, expected, module_name, is_backup = False):
        self.test_phrase = test_phrase.split(';')
        self.points = float(points)
        self.expected = eval(expected) if not is_backup else expected
        self.time_to_compute_actual = 0
        self.actual = None
        self.score = 0.0
        self.note = ''
        self.module_name = module_name
        self.module = None
        self.backup = None

    def compile(self):
        """Tries to import the module for testing its' content"""

        try:
            self.module = importlib.import_module(self.module_name, package=None)
            return True
        except Exception as e:
            compilation_error = str(e)
            self.note += 'Could not compile the file. The exception got was: "' + str(compilation_error) + '"' + \
                        ' (-' + str(self.points) + ')'
            self.score = 0
            return False

    def run_test(self):
        """runs all the test phrases. Saves to self.actual what is returned during the run of the last test phrase"""

        # makes sure nothing is printed during test
        sys.stdout = actual_print = ListStream()

        for i in range(len(self.test_phrase)):
            try:
                if '=' in self.test_phrase[i]:
                    exec(self.test_phrase[i])
                else:
                    start = time.time()
                    self.actual = eval(self.test_phrase[i])
                    end = time.time()
                    self.time_to_compute_actual = end - start
            except (ValueError, TypeError, Exception, TimeoutError) as e:
                self.actual = e
                break

        # try to cast actual type to expected
        try:
            self.actual = type(self.expected)(self.actual)
        except (TypeError, ValueError) as e:
            pass  # types not compatible

        # let printing occur again
        del actual_print
        sys.stdout = sys.__stdout__

    def check_types(self):
        """Checks if self.actual and self.expected are of the same type."""

        expected_class = type(self.expected)

        if not isinstance(self.actual, expected_class):
            self.note += 'On test: ' + str(self.test_phrase) + \
                        ' the value returned is not of the same type as expected. ' + \
                        'Should have returned object of type ' + str(type(self.expected)) + \
                        '. Instead the object got was of type: ' + str(type(self.actual)) + \
                        ' (-' + str(self.points) + ')\n'
            return -1
        return 1

    def check_value(self):
        """Checks if self.actual and self.expected store the same values."""

        if self.actual != self.expected:
            self.note += 'On test: ' + str(self.test_phrase) + \
                        ' the value returned is not as expected. ' + \
                        'Should have returned: ' + str(self.expected) + \
                        '. Instead got: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'
        else:
            self.score = self.points

    def compare(self):
        """Compares self.actual to self.expected. First handles exceptions, than checks types, lastly checks values"""

        if isinstance(self.actual, Exception) and not isinstance(self.expected, Exception):
            if 'string_updateEO' in self.test_phrase[0]:
                self.test_phrase[0] = self.test_phrase[0].replace('string_updateEO', 'string_updaeEO')
                self.score, self.note = self.compile_run_and_compare()
            else:
                self.note += 'On test: ' + str(self.test_phrase) + \
                            ' an error accrued while trying to call the test. ' + \
                            'The exception got was: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'
        else:
            type_correct = self.check_types()

            if type_correct == 1:
                self.check_value()
            elif type_correct == 0:
                self.backup.score, self.backup.note = self.backup.compile_run_and_compare()
                if self.backup.score == 0:
                    self.backup_fail()
                else:
                    if self.backup.score > WRONG_CLASS_DEDUCTION:
                        self.score = self.backup.score - WRONG_CLASS_DEDUCTION
                        self.note += self.backup.note + '\nOn test: ' + str(self.test_phrase) + \
                        ' the value returned is not of the same type as expected. ' + \
                        'Should have returned object of type ' + str(type(self.expected)) + \
                        '. Instead the object got was of type: ' + str(type(self.actual)) + '.' \
                                     + self.backup_success() + ' Deducted for wrong type only (-' + str(WRONG_CLASS_DEDUCTION) + ')'

        return self.score, self.note

    def compile_run_and_compare(self):
        if not self.compile():
            return self.score, self.note
        self.run_test()
        return self.compare()

    def backup_success(self):
        pass

    def backup_fail(self):
        pass


class TestPrint(Test):

    def run_test(self):
        """runs all the test phrases. Saves to self.actual what is printed during the run of the last test phrase"""
        for i in range(len(self.test_phrase)):
            # makes sure the printed output is saved to a string
            sys.stdout = self.actual = ListStream()

            # running the test
            try:
                if '=' in self.test_phrase[i]:
                    exec(self.test_phrase[i])
                else:
                    eval(self.test_phrase[i])
                self.actual = self.actual.data[:-1]

            # handling exceptions
            except (ValueError, TypeError, Exception, TimeoutError) as e:
                self.actual = e
                break

        # let printing occur again
        sys.stdout = sys.__stdout__

    def check_value(self):
        """Checks if self.actual and self.expected store the somewhat similar strings"""

        success = False

        actual = self.actual
        expected = self.expected

        if 'magic' in self.test_phrase[0]:
            actual = re.sub(r'0+(.+)', '', re.sub('[^0-9]', '', self.actual))
            expected = re.sub('[^0-9]', '', self.expected)

            if compare_strings(actual, expected) or actual in expected:
                success = True
        elif 'chose_password' in self.test_phrase[0]:
            actual = self.actual.replace("""'""", '').lower()
            expected = self.expected.replace("""'""", '').lower()

            if compare_strings(actual, expected):
                success = True
        else:
            if compare_strings(actual, expected):
                success = True

        if success:
            self.score = self.points
        else:
            self.handle_fail()

    def handle_fail(self):
        if str(self.actual) == '':
            self.backup = TestList(';'.join(self.test_phrase), self.points, list(self.expected), self.module_name,
                                   is_backup=True)
            self.score, self.note = self.backup.compare()
        else:
            too_long_value = 100
            diff = len(self.actual) - len(self.expected)
            if diff > too_long_value:
                self.note += 'On test: ' + str(self.test_phrase) + \
                             ' printing is not right. Should have printed "' + str(self.expected) + \
                             '". Instead printed a string which is a ' + str(diff) + \
                             ' chars longer than expected and is too big to print out.' \
                             + ' (-' + str(self.points) + ')\n'
            else:
                if 'magic' in self.test_phrase[0]:
                    self.note += 'On test: ' + str(self.test_phrase) + \
                                 ' printing is not right. Should have printed a string CONTAINING (in some way) the ' \
                                 'following stream:"' + str(self.expected) + \
                                 '". Instead printed: "' + str(self.actual) + '"' + ' (-' + str(self.points) + ')\n'
                else:
                    self.note += 'On test: ' + str(self.test_phrase) + \
                                 ' printing is not right. Should have printed "' + str(self.expected) + \
                                 '". Instead printed: "' + str(self.actual) + '"' + ' (-' + str(self.points) + ')\n'


class TestList(Test):
    def check_types(self):
        if isinstance(self.actual, type(None)) and not self.backup:
            self.backup = TestPrint(';'.join(self.test_phrase), self.points, str(self.expected), self.module_name,
                                    is_backup=True)
            return 0
        else:
            return super().check_types()

    def check_value(self):
        """Checks if self.actual and self.expected store the same elements, without respect to order."""

        if collections.Counter(self.actual) != collections.Counter(self.expected):
            self.note += 'On test: ' + str(self.test_phrase) + \
                        ' the list/tuple/dictionary returned is not as expected. ' + \
                        'Should have returned: ' + str(self.expected) + \
                        '. Instead got: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'
        else:
            self.score = self.points
            # if self.backup:
            #     self.note += 'On test: ' + str(self.test_phrase) + ' should have printed but returned a list (-2)'
            #     self.score -= 2

    def backup_success(self):
        return ' Tried a backup test to see if the list was instead printed correctly - which it did.'

    def backup_fail(self):
        self.note += 'On test: ' + str(self.test_phrase) + \
                        ' the value returned is not of the same type as expected. ' + \
                        'Should have returned object of type ' + str(type(self.expected)) + \
                        '. Instead the object got was of type: ' + str(type(self.actual)) + '.' + \
                        ' Tried a backup test to see if the returned object was printed correctly but got the ' \
                        'following issue: ' + re.sub(r'\([^)]*\)', '', str(self.backup.note)) + \
                        ' (-' + str(self.points) + ')\n'


class TestNumberOrBoolean(Test):
    def check_types(self):
        """Checks if self.actual and self.expected are of the same type.
        If not, tries to cast self.actual to the type of self.expected"""

        if not isinstance(self.actual, type(self.expected)):
            try:
                self.actual = type(self.expected)(self.actual)
                return True
            finally:
                return super(TestNumberOrBoolean, self).check_types()
        return True


class TestException(Test):
    def compare(self):
        """Compares if self.actual and self.expected are the same type of exception"""

        if not isinstance(self.actual, type(self.expected)):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' the exception returned is not correct. Should have returned exception of type ' + \
                        str(type(self.expected)) + '. Instead the exception got was: ' + str(self.actual)
        else:
            self.score = self.points
        return self.score, self.note


class TestString(Test):
    def check_value(self):
        """Checks if self.actual and self.expected store the somewhat similar strings"""

        if compare_strings(self.actual, self.expected):
            self.score = self.points
        else:
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' the string returned is not as expected. Should have returned "' + str(self.expected) + \
                        '". Instead returned: "' + str(self.actual) + '"'


class TestUpperFile(Test):
    """Special test for the upper_file task.
    The test checks if there is a file named with id in output directory.
    It also checks if the content of the file is a string the same as self.expected.
    Eventually the test deletes the file that was created during the test."""

    def __init__(self, test_phrase, points, expected, module_name):
        """In addition to the regular Test init, also initializes the path_to_file field"""

        super(TestUpperFile, self).__init__(test_phrase, points, expected, module_name)
        self.path_to_file = None

    def set_path_to_file(self):
        """Sets the path to the file that should be created during test.
        If directory does not exists, creates it."""

        id_num = str(re.search("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", self.module.FILE_NAME).group(0))
        self.path_to_file = 'output/upper_file_' + str(id_num) + '.txt'
        if not os.path.exists('output'):
            os.mkdir('output')

    def run_test(self):
        """Before runing the test, sets the path to file"""

        self.set_path_to_file()
        super(TestUpperFile, self).run_test()

    def compare(self):
        if isinstance(self.actual, Exception):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' an error accrued while trying to call the test. ' + \
                        'The exception got was: ' + str(self.actual)

        elif not os.path.exists(self.path_to_file):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' should have created file: "' + str(self.path_to_file) + '",' + \
                        'but file does not exists'

        else:
            file_to_check = open(self.path_to_file, 'r')
            line = file_to_check.read().splitlines()[0]
            if not compare_strings(line, self.expected, 2):
                self.note = 'On test ' + str(self.test_phrase) + \
                            ': the string in the file is not correct. ' + \
                            'The string should have been: "' + str(self.expected) + \
                            '". Instead wrote: "' + str(line) + '"'
                file_to_check.close()

            else:
                self.score = self.points
        if os.path.exists(self.path_to_file):
            os.remove(self.path_to_file)
        return self.score, self.note


class TestNumpy(Test):
    def check_value(self):
        """Checks the valus of self.actual and self.expected as numpy arrays."""

        if not np.array_equal(np.around(self.actual), np.around(self.expected)):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' the numpy array returned is not as expected. ' + \
                        'Should have returned: ' + str(self.expected) + \
                        '. Instead got: ' + str(self.actual)
        else:
            self.score = self.points


TEST_TYPES_DICT = {'PRINT_TEST_TYPE': TestPrint,
                   'LIST_TEST_TYPE': TestList,
                   'ORDERED_LIST_TEST_TYPE': Test,
                   'TUPLE_TEST_TYPE': TestList,
                   'ORDERED_TUPLE_TEST_TYPE': Test,
                   'DICT_TEST_TYPE': TestList,
                   'BOOL_TEST_TYPE': TestNumberOrBoolean,
                   'NUMBER_TEST_TYPE': TestNumberOrBoolean,
                   'EXCEPTION_TEST_TYPE': TestException,
                   'UPPER_FILE_TEST_TYPE': TestUpperFile,
                   'STRING_TEST_TYPE': TestString,
                   'NUMPY_TEST_TYPE': TestNumpy}
