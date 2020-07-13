#  Checker

A python tool dedicated to test python codes according to some test file.
This tool automatically checks a bunch of python assignments, grade them and outputs a xlsx file with grades and notes.

## How it works?
### Arguments:
The checker needs arguments to function:
1. **(Reqierd)** **path** - Path to the assignments needed to be checked.
2. **(Reqierd)** **test_file** - Path to test file containing all the tests needed to be tested.
3. (Optional)  **save_to** - Directory to save the copied assignments to.
**WARNING**: Whatever in this directory will be DELETED. 
default = 'tested/' 
4. (Optional) **workbook** - Directory to save xlsx file with scores and notes. This argument must have '.xlsx' suffix. 
default = './Assignment Grades.xlsx' 
5. (Optional) **sheet_title** - Title for the workbook sheet where the scores and notes 
will be written. 
default = 'Assignment Students Grades'

### What does it do?
   1. Clears **save_to** and get it ready to host all the assignments files that will be imported for testing.
   2.  Clears code of assignments files from **path** and save it to **save_to**.
   3. Creates **workbook** with a sheet named **sheet_title** to write scores and notes to it.
   4. Reads the **test_file** and extract data from it.
   5. Runs the tests for each file in **save_to**, and writes the score and notes it got to **workbook**.

# Test File
The **test_file** must have a specific format, in order for the checker to be able to read it.
- The tests file name must have '.csv' suffix. 
- First line in the file is: 
	`'TestPhrase|Points|ExpectedValue|TestType'`
	* (overall the first line is ignored).
- Every other line should be a different test with arguments separated with `|`: 
    - **TestPhrase** - A bunch of commands separated with `;`. 
	    - Calling an object form the file to test should have the prefix `self.module.`
    - **Points** - How many points the test worth. 
	    - Must be integer or float. 
    - **ExpectedValue** - The value expected to return from the test. 
    - **TestType** - Usually the type of the expected output. 
	     - For instance: 
	     `STRING_TEST_TYPE`
	     `PRINT_TEST_TYPE`
	     `LIST_TEST_TYPE`
	     - Try ' -t' for a list of test types.
	     - Hint: if you are not using a test type from the list, the comparison between the expected value and the actual returned value will be `==`.
- File must not have any other lines that are not tests of the form mentioned above. Empty lines are forbidden. 
- Examples: 
`x = -1;self.module.compute_roots(x)|7|ValueError()|EXCEPTION_TEST_TYPE`
`home = self.module.Location(2.5, 3.0);str(home)|5|"2.5_3.0"|STRING_TEST_TYPE`
`self.module.isSumDivided(12987)|8|int(54)|NUMBER_TEST_TYPE`
`self.module.triangle(-10)|6|"Wrong value"|PRINT_TEST_TYPE`

### Implemented Tests Types:
    PRINT_TEST_TYPE
    LIST_TEST_TYPE
    ORDERED_LIST_TEST_TYPE
    TUPLE_TEST_TYPE
    ORDERED_TUPLE_TEST_TYPE
    DICT_TEST_TYPE
    BOOL_TEST_TYPE
    NUMBER_TEST_TYPE
    EXCEPTION_TEST_TYPE
    UPPER_FILE_TEST_TYPE
    STRING_TEST_TYPE
    NUMPY_TEST_TYPE
If you are not using a test type from the list, the comparison between the expected value and the actual returned value will be '=='.
If you want to add your own test type, it should be added to the `tests_classes.py` file.
Each unique test is a python class inheriting from the class `Test` implemented in that file. 

# How to use?
1. Clone this repository.
2. Run setup from the repository root directory.
3. From the repository directory run:
`python checker.py test [path/to/assignments/] [path/to/test_file.csv]`

## Running tips:
* for help on how to use run:
`python checker.py -h`

* for instructions how to write the tests file run:
`python checker.py -i`

* for the tests types implemented run:
`python checker.py -t`

* to run with the optional arguments run:
`python checker.py test [path/to/assignments/] [path/to/test_file.csv] 
--save_to=[/path/to/save/copied/assignments/] --workbook=[/path/to/workbook.xlsx] --sheet_title=[Grades]`

