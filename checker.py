import utils
import my_parser


def read_copy_run(path, out_path, workbook_path, sheet_name, test_path):
    """Calls other functions to:
    (1) Clear out_path and get it ready to host all the assignments files that will be imported for testing.
    (2) Clear code of assignments files from path and save it to out_path.
    (3) Create workbook with a sheet named sheet_name to write scores and notes to it.
    (4) Read the tests file and extract data from it.
    (5) Run the tests for each file in out_path, and writes the score and notes it got to workbook"""

    utils.clean_out_path(out_path)
    utils.copy_assignments(path, out_path)
    utils.create_workbook(workbook_path, sheet_name)
    tests, points, expected, test_types = utils.read_tests(test_path)
    utils.run_write(out_path, workbook_path, tests, points, expected, test_types, flag_print=True)


if __name__ == "__main__":

    parser = my_parser.my_parser()
    args = parser.parse_args()

    # print instructions for tests file and exit
    if args.instructions:
        print(my_parser.INSTRUCTIONS)
        exit()

    # print TEST_TYPES and exit
    elif args.TEST_TYPES:
        print(my_parser.TEST_TYPES_INSTRUCTIONS)
        exit()

    # if no arguments were given - exit.
    elif len(vars(args).keys()) == 2:
        exit()

    # apply the checker
    else:

        # Check if arguments are legal. If not - exit.
        my_parser.check_args(args)

        # save the arguments to variables
        assignments_path = args.path
        tests_path = args.tests
        path_to_save_copied_assignments = args.save_to
        workbook_path = args.workbook
        sheet_title = args.sheet_title

        # run the program
        read_copy_run(assignments_path, path_to_save_copied_assignments, workbook_path, sheet_title, tests_path)
