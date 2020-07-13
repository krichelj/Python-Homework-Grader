import os
import re
import argparse
import textwrap
import tests_classes


# input checks functions:
def check_path(path):
    """Checks if the path to assignments files is legal and not empty"""

    if not os.path.exists(path):
        return False, "The assignments directory does not exists."
    if len(os.listdir(path)) == 0:
        return False, "The assignments directory is empty"
    return True, ""


def check_workbook_path(path_to_workbook_path):
    """Checks if the path to workbook is legal"""

    if path_to_workbook_path[-5:] != '.xlsx':
        return False, "Path to workbook is not legal: should have 'xlsx' suffix."
    return True, ""


def check_line_legal(line, j):
    """Checks a line in tests file, if all its' parameter are legal """

    warning = ""
    params = line.strip("\n").split("|")
    test = params[0]
    points = params[1]
    expected = params[2]
    test_types = params[3]

    # checking the points is a number
    if re.match(r'^-?\d+(?:\.\d+)?$', points) is None:
        return False, "Test file is not legal: in line " + str(j) + " the points are not float or integer. " +\
                       "Use '-i' for instructions"

    # checking that there is only one phrase in points, expected and test type
    if ';' in points or ';' in expected or ';' in test_types:
        return False, "Test file is not legal: in line " + str(j) +\
                      " ';' symbol can appear only in test phrase. " +\
                      "Use '-i' for instructions"

    # warning if a test phrase has no effect.
    if 'self.module.' not in test:
        warning = "WARNING: in test file, in line " + str(j) + " there is no 'self.module.' call. " +\
                  "This line will not test anything. \n"

    return True, warning


def check_tests_file_path(path_to_tests):
    """Checks if the test file exists and legal.
    If it is not, returns a helpful message."""

    # checking if the file path is legal
    if not os.path.isfile(path_to_tests):
        return False, "Tests path is not a file"
    if path_to_tests[-4:] != '.csv':
        return False, "Tests path must have a '.csv' suffix"

    # checking the content of the file
    legality, message = True, ""
    tests_file = open(path_to_tests)
    for j, line in enumerate(tests_file):
        # first line is ignored
        if j == 0:
            continue

        # checking if there are empty lines
        if line == '' or line == '\n':
            return False, "Test file is not legal: line " + str(j) + \
                          " is empty. File cannot have empty lines. " + \
                          "Use '-i' for instructions"

        # checking each line has exactly four parts divided by '|'
        if line.count('|') != 3:
            return False, "Test file is not legal: in line " + str(j) + \
                          " there should be exactly three '|' symbols. " + \
                          "Use '-i' for instructions"

        # checking if the parameters given are legal
        legality, message = check_line_legal(line, j)
        if not legality:
            return legality, message
    return legality, message


SUB_PARSER_HELP = """test = Start test. Must accept arguments: path tests_file.
path = Directory to where the assignments are stored. 
       for instance: /path/to/assignments/ 
tests_file = Directory to tests file. 
             for instance: /path/to/tests_file.csv 
--save_to = Directory to save the copied assignments to. 
            WARNING: Whatever in this directory will be DELETED. 
            for instance: /path/to/save/copied/assignments/ 
            default = 'tested/' 
--workbook = Directory to save xlsx file with scores and notes. 
             Should have '.xlsx' suffix. 
             for instance: /path/to/workbook.xlsx 
             default = './Assignment Grades.xlsx' 
--sheet_title = Title for the workbook sheet where the scores and notes 
will be written. 
                for instance: Grades 
                default = 'Assignment Students Grades'"""

INSTRUCTIONS = """Instructions how to write the tests csv document:
-------------------------------------------------
The tests file must have '.csv' suffix. 
File should have the following format: 
First line is: 'TestPhrase|Points|ExpectedValue|TestType' (overall the fist line is ignored).
Every other line should be a different test with arguments separated with '|': 
    Test Phrase = A bunch of commands separated with ';'. 
                  Calling an object form the file to test should have the prefix 'self.module.'
    Points = How many points the test worth. should be integer or float. 
    Expected value = The value expected to return from the test. 
    Test type = Usually the type of the expected output. 
                For instance: 'STRING_TEST_TYPE', 'PRINT_TEST_TYPE', 'LIST_TEST_TYPE'...
                Try '-t' for a list of test types.
                Hint: if you are not using a test type from the list, 
                      the comparison between the expected value and the actual returned value will be '=='.
File must not have any other lines that are not tests of the form mentioned above. Empty lines are forbidden. 
Example: 'x = -1;self.module.compute_roots(x)|7|ValueError()|EXCEPTION_TEST_TYPE'
"""

TEST_TYPES_INSTRUCTIONS = """Available test types: \n""" +\
    """---------------------\n    """ +\
    str('\n    '.join(list(tests_classes.TEST_TYPES_DICT.keys()))) +\
    """\n If you are not using a test type from the list, the comparison between the expected value """ +\
    """and the actual returned value will be '=='."""


def my_parser():
    parser = argparse.ArgumentParser(description='Python assignments code checker.',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     usage="checker.py [-h] [-i] [-t] \n"
                                           "usage: checker.py test path tests_file "
                                           "[--save_to] [--workbook] [--sheet_title] \n")

    parser.add_argument('-i', '--instructions',
                        action='store_true',
                        help=textwrap.dedent("""show instructions how to write the tests file"""))

    parser.add_argument('-t', '--TEST_TYPES',
                        action='store_true',
                        help=textwrap.dedent("""show test types available for test"""))

    subparsers = parser.add_subparsers(help=SUB_PARSER_HELP)

    parser_a = subparsers.add_parser('test',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     usage="checker.py test path tests_file "
                                           "[--save_to] [--workbook] [--sheet_title] \n")

    parser_a.add_argument("path",
                          metavar="/path/to/assignments/",
                          help="Directory to where the assignments are stored")
    parser_a.add_argument("tests",
                          metavar="/path/to/tests_file.csv",
                          help="Directory to tests file.")
    parser_a.add_argument('--save_to',
                          default='tested/',
                          metavar="/path/to/save/copied/assignments/",
                          help='Directory to save the copied assignments to. '
                               'Whatever in this directory will be deleted')
    parser_a.add_argument('--workbook',
                          default='./Assignment Grades.xlsx',
                          metavar="/path/to/workbook.xlsx",
                          help='Directory to save xlsx file with scores and notes. Should have ".xlsx" suffix.')
    parser_a.add_argument('--sheet_title',
                          default="Assignment Students Grades",
                          metavar="Grades",
                          help='Title for the workbook sheet where the scores and notes will be written.')

    def my_error(message):
        print(message)
        exit()

    parser_a.error = my_error
    parser.error = my_error

    return parser


def check_args(args):
    assignments_path = args.path
    tests_path = args.tests
    workbook_path = args.workbook

    # check if all arguments are legal
    legal_path, message_path = check_path(assignments_path)
    if not legal_path:
        print(message_path)
        exit()

    legal_tests, message_tests = check_tests_file_path(tests_path)
    if not legal_tests:
        print(message_tests)
        exit()

    legal_workbook, message_workbook = check_workbook_path(workbook_path)
    if not legal_workbook:
        print(message_workbook)
        exit()

    if message_tests:
        print(message_tests)
