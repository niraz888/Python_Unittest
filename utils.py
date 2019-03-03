"""
Const Names
"""
# properties of customer
FIRST_NAME = 0
LAST_NAME = 1
EMAIL = 2
PASSWORD = 3
MOBILE = 4
COUNTRY = 5
ADDRESS_1 = 6
ADDRESS_2 = 7
STATUS = 8

# Login window properties
LOGIN_MAIL = 0
LOGIN_PASS = 1

# index of args in the (test No.) -> args mapper
ARGS_FOR_TEST_1 = 1
ARGS_FOR_TEST_2 = 2
ARGS_FOR_TEST_3 = 3
ARGS_FOR_TEST_4 = 4
ARGS_FOR_TEST_5 = 5
ARGS_FOR_TEST_6 = 6
ARGS_FOR_TEST_7 = 7
ARGS_FOR_TEST_8 = 8

# etc.
NUMBER_OF_PAGES = 9
TIME_WAIT_FOR_PAGE_LOAD = 10


"""
Util class.
have a mapper that maps between test number (1,2,3..) and a list of args
for this test.
"""


class Util(object):
    def __init__(self):
        self.mapper = {}

    def start(self, file_name):
        i = 1
        with open(file_name, 'r') as input_file:
            content = input_file.readlines()
            for line in content:
                line.strip('\n')
                arr = line.split(';')
                size = len(arr)
                arr[size - 1] = arr[size-1].replace("\n", "")
                self.mapper[i] = arr
                i += 1
