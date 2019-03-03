#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ex
from selenium.webdriver.common.keys import Keys
import unittest
from utils import Util
from unittest import TestLoader, TextTestRunner, TestSuite
from test_class import *
import time

"""
Unit1 class.
include all Tests that related to the login window
"""


class Unit1(unittest.TestCase):
    # set the environment for tests
    def setUp(self):
        self.tester = TestUnit1()
        self.util = Util()
        self.util.start('inputs')

    # Test 1
    def test_if_enter_well(self):
        try:
            self.assertEqual('Connected Successfully', self.tester.sign_in(
                self.util.mapper[ARGS_FOR_TEST_1][LOGIN_MAIL], self.util.mapper[ARGS_FOR_TEST_1][LOGIN_PASS]))
        except Exception as e:
            print('Test 1 Failed Because ' + str(e))

    # Test 2
    def test_if_doesnt_enter_bad_credentials(self):
        try:
            self.assertEqual('Invalid Login Credentials', self.tester.sign_in(
                self.util.mapper[ARGS_FOR_TEST_2][LOGIN_MAIL], self.util.mapper[ARGS_FOR_TEST_2][LOGIN_PASS]))
        except Exception as e:
            print('Test 2 Failed Because ' + str(e))

    # Test 3
    def test_if_doesnt_enter_with_invalid_email(self):
        expected_res = 'The Email field must contain a valid email address.'
        try:
            self.assertEqual(expected_res, self.tester.sign_in(
                self.util.mapper[ARGS_FOR_TEST_3][LOGIN_MAIL], self.util.mapper[ARGS_FOR_TEST_3][LOGIN_PASS]))
        except Exception as e:
            print('Test 3 Failed because ' + str(e))

    # Test 4
    def test_if_doesnt_enter_with_blank(self):
        try:
            self.assertFalse(self.tester.sign_in(
                self.util.mapper[ARGS_FOR_TEST_4][LOGIN_MAIL], self.util.mapper[ARGS_FOR_TEST_4][LOGIN_PASS]))
        except Exception as e:
            print('Test 4 Failed because ' + str(e))

    def tearDown(self):
        self.tester.shutdown_driver()


"""
Unit2 class.
include all tests that related to the action of add and delete a customer
"""


class Unit2(unittest.TestCase):

    def setUp(self):
        self.tester = TestUnit2()
        self.util = Util()
        self.util.start('inputs')

    # Test 5
    def test_add_customer_with_short_password(self):
        try:
            customer = Customer(self.util.mapper[ARGS_FOR_TEST_5])
            array_of_errors = self.tester.add_and_check_customer(customer)
            self.assertIn('The Password field must be at least 6 characters in length.', array_of_errors)
        except Exception as e:
            print('Test 5 Failed because ' + str(e))

    # Test 6
    def test_add_customer_with_name_field_missing(self):
        try:
            customer = Customer(self.util.mapper[ARGS_FOR_TEST_6])
            array_of_errors = self.tester.add_and_check_customer(customer)
            self.assertIn('The First Name field is required.', array_of_errors)
        except Exception as e:
            print('Test 6 Failed because' + str(e))

    # Test 7
    def test_add_customer_correctly(self):
        try:
            customer = Customer(self.util.mapper[ARGS_FOR_TEST_7])
            array_of_notes = self.tester.add_and_check_customer(customer)
            self.assertIn('Customer Added Successfully', array_of_notes)
        except Exception as e:
            print('Test 7 Failed because ' + str(e))

    # Test 8
    def test_if_customer_deleted_successfully(self):
        try:
            customer = Customer(self.util.mapper[ARGS_FOR_TEST_8])
            self.tester.entry()
            self.tester.navigate_to_customers_addition()
            self.assertEqual('Success', self.tester.delete_customer(customer))
        except Exception as e:
            print('Test 7 Failed because ' + str(e))

    def tearDown(self):
        self.tester.shutdown_driver()

"""
Unit3 class.
include all tests that related to the log out action
"""


class Unit3(unittest.TestCase):

    def setUp(self):
        self.tester = TestUnit2()
        self.util = Util()
        self.util.start('inputs')

    # Test 9
    def test_if_log_out_successfully(self):
        try:
            self.tester.entry()
            self.tester.sign_out()
        except Exception as e:
            print('Test 8 Failed because ' + str(e))

    def tearDown(self):
        self.tester.shutdown_driver()


if __name__ == '__main__':
    loader = TestLoader()
    suite = TestSuite((
         loader.loadTestsFromTestCase(Unit1),
        loader.loadTestsFromTestCase(Unit2),
        loader.loadTestsFromTestCase(Unit3)
    ))
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
