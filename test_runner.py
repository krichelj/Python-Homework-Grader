import os

if __name__ == "__main__":
    ass = 3
    os.system("TASKKILL /F /IM EXCEL.exe")
    submission_locations = {1: 'assignments/1/submissions/tmp/',
                            2: 'assignments/2/submissions/',
                            3: 'assignments/3/submissions/'}
    test_files = {1: 'assignments/1/tests1.csv',
                  2: 'assignments/2/tests2.csv',
                  3: 'assignments/3/tests3.csv'}
    output_files = {1: 'assignments/1/output_tmp',
                    2: 'assignments/2/ass2grades',
                    3: 'assignments/3/ass3grades'}

    os.system('python checker.py test ' + submission_locations[ass] +
              ' ' + test_files[ass] + ' --workbook=' + output_files[ass] + '.xlsx')
    os.system('python checker.py test ' + submission_locations[ass] + 'stuck/'
              ' ' + test_files[ass] + ' --workbook=' + output_files[ass] + '_stuck.xlsx')
    # os.system('start EXCEL.exe ' + output_files[ass])
