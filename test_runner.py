import os

if __name__ == "__main__":
    ass = 2
    os.system("TASKKILL /F /IM EXCEL.exe")
    submission_locations = {1: 'assignments/1/submissions/tmp/',
                            2: 'assignments/2/submissions/'}
    test_files = {1: 'assignments/1/tests1.csv',
                  2: 'assignments/2/tests2.csv'}
    output_files = {1: 'assignments/1/output_tmp.xlsx',
                    2: 'assignments/2/ass2grades.xlsx'}

    os.system('python checker.py test ' + submission_locations[ass] +
              ' ' + test_files[ass] + ' --workbook=' + output_files[ass])
    # os.system('start EXCEL.exe ' + output_files[ass])
