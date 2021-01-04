import os
from time import time

if __name__ == "__main__":
    start_time = time()
    ass = 4
    os.system("TASKKILL /F /IM EXCEL.exe")

    submission_locations = {1: 'assignments/1/resubmissions/',
                            2: 'assignments/2/resubmissions/',
                            3: 'assignments/3/resubmissions/',
                            4: 'assignments/4/submissions/'}

    test_files = {1: 'assignments/1/tests1.csv',
                  2: 'assignments/2/tests2.csv',
                  3: 'assignments/3/tests3.csv',
                  4: 'assignments/4/tests4.csv'}

    output_files = {1: 'assignments/1/ass1regrades',
                    2: 'assignments/2/ass2regrades',
                    3: 'assignments/3/ass3regrades',
                    4: 'assignments/4/ass4grades'}

    os.system('python checker.py test ' + submission_locations[ass] +
              ' ' + test_files[ass] + ' --workbook=' + output_files[ass] + '.xlsx')
    # os.system('python checker.py test ' + submission_locations[ass] + 'stuck/'
    #           ' ' + test_files[ass] + ' --workbook=' + output_files[ass] + '_stuck.xlsx')
    print(time() - start_time)
    # os.system('start EXCEL.exe ' + output_files[ass])
