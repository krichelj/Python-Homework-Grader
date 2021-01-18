import sys
import os
import re
import difflib
import importlib
import collections
import numpy as np
import time
from typing import Union
import itertools

from RecursionDetector import test_recursion
from LoopDetector import uses_loop
from Timeout import timeout

WRONG_CLASS_DEDUCTION = 0.5


class ListStream:
    """this class enables to save as a string everything that was printed"""

    def __init__(self):
        self.data = ''

    def write(self, s):
        self.data = self.data + s

    def flush(self):
        pass


def compare_strings(out_str, expected_str, difference_num=5):
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
    def __init__(self, assignment_num: int, test_phrase: str, points, expected, module_name, testing_stuck=False,
                 is_backup=False):
        self.assignment_num = assignment_num
        self.test_phrase = test_phrase.split(';')
        self.points = float(points)
        self.expected = eval(expected) if not (is_backup or isinstance(self, (TestClass, TestMethod))) else expected
        self.time_to_compute_actual = 0
        self.actual = None
        self.score = 0.0
        self.note = ''
        self.module_name = module_name
        self.module = None
        self.testing_stuck = testing_stuck
        self.backup: Union[Test, None] = None
        self.is_backup = is_backup
        self.is_recursive = False

    def compile(self):
        """Tries to import the module for testing its' content"""

        try:
            self.module = importlib.import_module(self.module_name, package=None)
            return True
        except Exception as e:
            compilation_error = str(e)
            self.note = 'Could not compile the file. The exception got was: "' + str(compilation_error) + '"' + \
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
            if isinstance(self, TestPrint):
                self.note = 'On test: ' + str(self.test_phrase) + ' there was supposed to be a print. ' + \
                            'Instead returned an object of type: ' + str(type(self.actual)) + \
                            ' (-' + str(self.points) + ')\n'
            # if isinstance(self.actual, type(None)) and not self.backup:
            #     self.backup = TestPrint(self.assignment_num, ';'.join(self.test_phrase), self.points,
            #                             self.backup_print_def(), self.module_name, is_backup=True)
            #     return 0
            else:
                self.note = 'On test: ' + str(self.test_phrase) + \
                            ' the value returned is not of the same type as expected. ' + \
                            'Should have returned object of type ' + str(type(self.expected)) + \
                            '. Instead the object got was of type: ' + str(type(self.actual)) + \
                            ' (-' + str(self.points) + ')\n'
            return -1
        return 1

    def check_value(self):
        """Checks if self.actual and self.expected store the same values."""

        if self.actual != self.expected:
            self.note = 'On test: ' + str(self.test_phrase) + \
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
                self.score, self.note, self.points = self.compile_run_and_compare()
            else:
                self.note = 'On test: ' + str(self.test_phrase) + \
                            ' an error accrued while trying to call the test. ' + \
                            'The exception got was: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'
        else:
            type_correct = self.check_types()

            if type_correct == 1:
                self.check_value()

                if self.assignment_num == 3 and 'permutation' not in self.test_phrase[0]:
                    def f():
                        return eval(self.test_phrase[0])

                    is_recursive = test_recursion(f)
                    uses_loops = uses_loop(f)

                    if (not is_recursive) and uses_loops:
                        non_recursive_reduction = int(self.points / 2)
                        if self.score > non_recursive_reduction:
                            self.score -= non_recursive_reduction
                        self.note += 'On test: ' + str(
                            self.test_phrase) + ' the function implemented is not recursive. ' + \
                                     'Half of the points deducted. (-' + str(non_recursive_reduction) + ')'

            # elif type_correct == 0:
            #     self.backup.score, self.backup.note = self.backup.compile_run_and_compare()
            #     if self.backup.score == 0:
            #         self.backup_fail()
            #     else:
            #         if self.backup.score > WRONG_CLASS_DEDUCTION:
            #             self.score = self.backup.score - WRONG_CLASS_DEDUCTION
            #             self.note = self.backup.note + '\nOn test: ' + str(self.test_phrase) + \
            #                          ' the value returned is not of the same type as expected. ' + \
            #                          'Should have returned object of type ' + str(type(self.expected)) + \
            #                          '. Instead the object got was of type: ' + str(type(self.actual)) + \
            #                         '. Tried a backup test to see if the object was instead printed correctly ' \
            #                         '- which it did. Deducted for wrong type only (-' \
            #                         + str(WRONG_CLASS_DEDUCTION) + ')'

        return self.score, self.note

    def compile_run_and_compare(self):
        if not self.compile():
            return self.score, self.note, self.points

        if not self.testing_stuck:
            self.run_test()
        else:
            time_out = 1
            func = timeout(seconds_before_timeout=time_out)(self.run_test)
            try:
                func()
            except:
                self.note = 'The test ' + str(self.test_phrase[0]) + ' failed due to a time out of ' + str(time_out) + \
                            ' seconds (-' + str(self.points) + ')'
                return self.score, self.note, self.points
        score, note = self.compare()
        return score, note, self.points

    def handle_wrong_value(self):
        pass

    def backup_print_def(self):
        return str(self.expected)

    def backup_fail(self):
        pass

    def __str__(self):
        return 'Ex: ' + str(self.assignment_num) + ', test: ' + str(self.test_phrase) + \
               ', backup: ' + str(self.is_backup)

    def check_for_char_occ(self, c: chr):
        return self.actual.count(c) == self.expected.count(c)


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
                if len(self.actual.data) > 1:
                    self.actual = self.actual.data[:-1]
                else:
                    self.actual = self.actual.data

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

        if 'triangle' in self.test_phrase[0]:
            actual = self.actual.replace(' ', '').replace('\n', '')
            expected = self.expected.replace(' ', '').replace('\n', '')

            if compare_strings(actual, expected) or actual in expected:
                success = True
        elif 'print_map' in self.test_phrase[0]:
            actual = self.actual.replace(' ', '').replace('\n', '')
            expected = self.expected.replace(' ', '').replace('\n', '')

            if not self.testing_stuck:
                success = compare_strings(actual, expected)
            else:
                time_out = 0.5
                func = timeout(seconds_before_timeout=time_out)(compare_strings)
                try:
                    success = func(actual, expected)
                except:
                    self.note = 'The test ' + str(self.test_phrase[0]) + ' failed due to a time out of ' + str(
                        time_out) + ' seconds (-' + str(self.points) + ')'



        elif 'magic' in self.test_phrase[0]:
            actual = re.sub('[^0-9]', '', self.actual)
            expected = re.sub('[^0-9]', '', self.expected)

            if compare_strings(actual, expected) or actual in expected:
                success = True
        elif 'chose_password' in self.test_phrase[0]:
            actual = self.actual.replace("""'""", '').lower()
            expected = self.expected.replace("""'""", '').lower()

            if compare_strings(actual, expected):
                success = True

        elif 'permutation' in self.test_phrase[0]:
            actual = self.actual.split('\n')
            lst_str = self.test_phrase[0].replace('self.module.permutation(', '').replace(')', '')
            lst = eval(lst_str)
            expected_first_line = 'The permutations of ' + str(lst_str) + ' are:'
            actual_first_line = str(actual[0])

            if not compare_strings(actual_first_line, expected_first_line):
                self.points -= 1
                self.note += "\nThe first line printed is not as expected. Should have printed: '" + expected_first_line \
                             + "', instead printed: '" + actual_first_line + "' (-1)\n"

            expected_permutations = set(itertools.permutations(lst))
            actual_permutations = set([tuple(eval(x)) for x in actual[1:]])

            if expected_permutations != actual_permutations:
                self.points -= 4
                self.note += 'The permutations printed are not as expected. ' \
                             'Should have printed the following permutations in some order: ' \
                             + str(expected_permutations) + '. Instead printed (in some order): ' \
                             + str(actual_permutations) + '.'

            self.score = self.points
        else:
            if compare_strings(actual, expected):
                success = True

        if 'permutation' not in self.test_phrase[0]:
            if success:
                self.score = self.points
            else:
                self.handle_wrong_value()

    def handle_wrong_value(self):
        # if str(self.actual) == '' and not self.is_backup:
        #     if 'is_ordered_list' in self.test_phrase[0]:
        #         self.backup = TestNumberOrBoolean(self.assignment_num, ';'.join(self.test_phrase), self.points,
        #                                           eval(self.expected), self.module_name, is_backup=True)
        #     elif 'one' in self.test_phrase[0]:
        #         self.backup = TestNumberOrBoolean(self.assignment_num, ';'.join(self.test_phrase), self.points,
        #                                           int(self.expected), self.module_name, is_backup=True)
        #     else:
        #         self.backup = TestList(self.assignment_num, ';'.join(self.test_phrase), self.points, [self.expected],
        #                                self.module_name, is_backup=True)
        #     self.backup.score, self.backup.note = self.backup.compile_run_and_compare()
        # else:
        #     too_long_value = 100
        #     diff = len(self.actual) - len(self.expected)
        #     if diff > too_long_value:
        #         self.note = 'On test: ' + str(self.test_phrase) + \
        #                      ' printing is not right. Should have printed "' + str(self.expected) + \
        #                      '". Instead printed a string which is a ' + str(diff) + \
        #                      ' chars longer than expected and is too big to print out.' \
        #                      + ' (-' + str(self.points) + ')\n'
        #     else:
        #         if 'magic' in self.test_phrase[0]:
        #             self.note = 'On test: ' + str(self.test_phrase) + \
        #                          ' printing is not right. Should have printed a string CONTAINING (in some way) the ' \
        #                          'following stream:"' + str(self.expected) + \
        #                          '". Instead printed: "' + str(self.actual) + '"' + ' (-' + str(self.points) + ')\n'
        #         else:
        # if 'print_map' in self.test_phrase[0]:
        #     self.note = 'The map printing is not right' + ' (-' + str(self.points) + ')\n'
        # else:
        self.note = 'On test: ' + str(self.test_phrase) + \
                    ' printing is not right. Should have printed "' + str(self.expected) + \
                    '". Instead printed: "' + str(self.actual) + '"' + ' (-' + str(self.points) + ')\n'


class TestList(Test):

    def check_value(self):
        """Checks if self.actual and self.expected store the same elements, without respect to order."""

        def convert_numeric(tup):
            return (float(i) if i.lstrip('-').replace('.', '', 1).isdigit() else i for i in tup if isinstance(i, str))

        def evaluate(z):
            z_type = type(z)
            output = z_type()

            for x in z:
                y = x

                if isinstance(y, str):
                    try:
                        y = eval(y.lstrip('0'))
                    except (SyntaxError, NameError):
                        pass

                output += z_type([y])

            return output

        def is_list_not_valid(actual, expected):
            actual = evaluate(actual)
            expected = evaluate(expected)

            if any([isinstance(x, list) for x in actual]):
                return any([is_list_not_valid(a, e) for a, e in zip(actual, expected)])
            if any([isinstance(x, tuple) for x in actual]):
                return actual.count(None) != expected.count(None) or \
                       any([is_list_not_valid(a, e) for a, e in
                            zip(convert_numeric(actual), convert_numeric(expected))])
            # if any([isinstance(x, tuple) for x in actual]):
            #     return is_list_not_valid \
            #         ([(float(i) if i.lstrip('-').replace('.', '', 1).isdigit() else i for i in x)
            #           if x else x for x in actual], expected)
            try:
                res = len(actual) == len(expected) and collections.Counter(actual) != collections.Counter(expected)
            except:
                res = False
            return res

        if 'compute_roots' in self.test_phrase[0]:
            self.actual = list(map(lambda x: x.replace('!', '').lower() if isinstance(x, str) else x, self.actual))

        if is_list_not_valid(self.actual, self.expected):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' the list/tuple/dictionary returned is not as expected. ' + \
                        'Should have returned: ' + str(self.expected) + \
                        '. Instead got: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'
        else:
            self.score = self.points
            # if self.backup:
            #     self.note = 'On test: ' + str(self.test_phrase) + ' should have printed but returned a list (-2)'
            #     self.score -= 2

    def backup_print_def(self):
        return '[' + ', '.join([str(x) for x in self.expected]) + ']'

    def backup_fail(self):
        self.note = 'On test: ' + str(self.test_phrase) + \
                    ' the value returned is not of the same type as expected. ' + \
                    'Should have returned object of type ' + str(type(self.expected)) + \
                    '. Instead the object got was of type: ' + str(type(self.actual)) + '.' + \
                    ' Tried a backup test to see if the returned object was printed correctly but got the ' \
                    'following issue: ' + re.sub(r'\([^)]*\)', '', str(self.backup.note)) + \
                    ' (-' + str(self.points) + ')\n'


class TestNumberOrBoolean(Test):
    pass


class TestException(Test):
    def run_test(self):
        try:
            exec(self.test_phrase[0])
        except Exception as e:
            self.actual = (type(e), e.args[0] if len(e.args) else '')

    def compare(self):
        """Compares if self.actual and self.expected are the same type of exception"""
        if not self.actual or self.actual[0] != self.expected[0]:
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' the exception returned is not correct. Should have returned exception of type ' + \
                        str(self.expected[0]) + '. Instead returned an output of type: ' + \
                        (str(self.actual[0]) if self.actual else 'None') + ' (-' + str(self.points) + ')'
        elif (self.expected[0] == type(TypeError) and
              not (compare_strings(self.actual[1], self.expected[1]) or compare_strings(self.actual[1],
                                                                                        'type input invalid'))) \
                or (self.expected[0] == type(TypeError) and not compare_strings(self.actual[1], self.expected[1])):
            self.note = "On test: " + str(self.test_phrase) + \
                        " the exception message is not correct. Should have returned the following message: '" + \
                        str(self.expected[1]) + "'. Instead returned: '" + str(self.actual[1]) + "'"
            self.score = int(self.points / 2)
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
                        '". Instead returned: "' + str(self.actual) + ' (-' + str(self.points) + ')'


class TestUpperFile(Test):
    """Special test for the upper_file task.
    The test checks if there is a file named with id in output directory.
    It also checks if the content of the file is a string the same as self.expected.
    Eventually the test deletes the file that was created during the test."""
    bonuses = []

    def __init__(self, assignment_num, test_phrase, points, expected, module_name, testing_stuck):
        """In addition to the regular Test init, also initializes the path_to_file field"""

        super(TestUpperFile, self).__init__(assignment_num, test_phrase, points, expected, module_name, testing_stuck)
        self.path_to_file = None
        self.curr_id = None
        files = self.expected

        with open(files[0], 'r') as sol_file:
            self.expected = [TestUpperFile.clear_lines(sol_file)]
        with open(files[1], 'r') as reduced_sol_file:
            self.expected += [TestUpperFile.clear_lines(reduced_sol_file)]

    @staticmethod
    def clear_lines(file):
        lines_to_print = [x for x in file.read().splitlines() if len(x) and 'All routes:' not in x
                          and 'Routes matching request:' not in x]
        lines_to_test = [x.lower().replace(' ', '').replace('\n', '') for x in lines_to_print]

        return lines_to_test, lines_to_print

    def set_path_to_file(self):
        """Sets the path to the file that should be created during test.
        If directory does not exists, creates it."""

        id_num_search = re.search("[0-9]{9}", self.module.FILE_NAME)
        self.curr_id = id_num_search.group(0) if id_num_search else 'sol'

        self.path_to_file = 'itinerary_' + str(self.curr_id) + '_' + (
            '1' if 'flights1' in self.test_phrase[0] else '2') + '.txt'

    def run_test(self):
        """Before running the test, sets the path to file"""

        self.set_path_to_file()
        super(TestUpperFile, self).run_test()

        # for file in glob.glob('itinerary*'):
        #     print(file)
        if os.path.exists('itinerary.txt') and not os.path.exists(self.path_to_file):
            try:
                os.rename('itinerary.txt', self.path_to_file)
            except PermissionError:
                self.path_to_file = 'itinerary.txt'
        elif os.path.exists('itinerary') and not os.path.exists(self.path_to_file):
            os.rename('itinerary', self.path_to_file)

    def compare(self):
        if isinstance(self.actual, Exception):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' an error accrued while trying to call the test. ' + \
                        'The exception got was: ' + str(self.actual) + ' (-' + str(self.points) + ')\n'

        elif not os.path.exists(self.path_to_file):
            self.note = 'On test: ' + str(self.test_phrase) + \
                        ' should have created file: "' + str(self.path_to_file) + '",' + \
                        'but file does not exists'

        else:
            with open(self.path_to_file, 'r') as file_to_check:
                self.actual = TestUpperFile.clear_lines(file_to_check)

            results = {}

            for i, case in enumerate(self.expected):
                matching_lines_num = 0
                lines_to_test, lines_to_print = case

                total_lines_num = len(lines_to_test)

                note = ''
                for line_to_test, line_to_print in zip(lines_to_test, lines_to_print):

                    if not any([compare_strings(line_to_test, expected_line) for expected_line in self.actual[0]]):
                        note += 'On test ' + str(self.test_phrase) + \
                                ": the expected line '" + line_to_print + "' was not found in the output file\n"
                    else:
                        matching_lines_num += 1

                results[round(self.points * matching_lines_num / total_lines_num, 1)] = (i, note)

            self.score = max(results.keys())
            i, note = results[self.score]

            reduction = round(self.points - self.score, 1)
            self.note = note + '\n(-' + str(reduction) + ')\n\n' if reduction > 0 else '\n\n'

            if i == 0 and self.curr_id not in TestUpperFile.bonuses:
                TestUpperFile.bonuses.append(self.curr_id)
                self.score += 10
                self.note += '###### MAD RESPECT FOR DOING THE BONUS! (+10) #######\n'

        # if os.path.exists(self.path_to_file):
        #     os.remove(self.path_to_file)

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


class TestClass(Test):

    def __init__(self, assignment_num, test_phrase, points, expected, module_name, testing_stuck):
        super(TestClass, self).__init__(assignment_num, test_phrase, points, expected, module_name, testing_stuck)
        self.object_ref = self.test_phrase[0].split('=')[0][:-1]

    def run_test(self):
        try:
            exec(self.test_phrase[0])
        except (ValueError, TypeError, NameError) as e:
            self.actual = e

    def check_types(self):
        return 1

    def check_value(self):
        test_class = eval('self.module.' + self.expected)
        obj = eval(self.object_ref)

        if isinstance(obj, test_class):
            self.score = self.points


class TestMethod(Test):
    def run_test(self):
        try:
            self.actual = eval(self.test_phrase[0])
        except (AttributeError, ValueError, TypeError, UnboundLocalError) as e:
            self.actual = e

    def check_types(self):
        return 1

    def check_value(self):
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
                   'NUMPY_TEST_TYPE': TestNumpy,
                   'CLASS_TEST_TYPE': TestClass,
                   'METHOD_TEST_TYPE': TestMethod}

if __name__ == '__main__':
    print('''1
21
123
4321
12345
654321
1234567
87654321
123456789
10987654321'''.replace('\\n', '\n'))
