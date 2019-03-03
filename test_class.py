from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import unittest
import time
from utils import *


class TestUnit1(object):
    """
    TestUnit1 class.
    an helper class that his methods are responsible of testing the
    first step of assignment - the part of login
    """
    def __init__(self):
        self.driver = webdriver.Chrome('/home/nir/py/chromedriver')

    def sign_in(self, username, password):
        """
        sign_in method.
        sign in to the menu
        :param username:
        :param password:
        :return: message of the result of login
        """
        self.driver.get("https://www.phptravels.net/admin")
        self.driver.find_element_by_name('email').send_keys(username)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_css_selector('button').click()
        try:
            WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(expected_conditions.title_contains('Dashboard'))
        except Exception:
            err_elm = self.driver.find_element_by_xpath("//form/div[contains(@class, 'resultlogin')]").text
            return err_elm
        return 'Connected Successfully'

    def shutdown_driver(self):
        self.driver.close()


class Customer(object):
    """
    customer class.
    represent a given customer.
    """
    def __init__(self, args_for_customer):
        self.first_name = args_for_customer[FIRST_NAME]
        self.last_name = args_for_customer[LAST_NAME]
        self.email = args_for_customer[EMAIL]
        self.password = args_for_customer[PASSWORD]
        self.mobile = args_for_customer[MOBILE]
        self.country = args_for_customer[COUNTRY]
        self.address_1 = args_for_customer[ADDRESS_1]
        self.address_2 = args_for_customer[ADDRESS_2]
        self.status = args_for_customer[STATUS]


class TestUnit2(object):

    def __init__(self):
        self.driver = webdriver.Chrome('/home/nir/py/chromedriver')

    def add_and_check_customer(self, customer) -> list:
        """
        add_and_check_customer method.
        include the whole process of adding a customer -> reach to the appropriate page,
        fill the fields with customer's propperty and in the end check if it appear in
        table
        :param customer:
        :return: list of notes/warning
        """
        self.entry()
        self.navigate_to_customers_addition()
        res, notes = self.add_customer(customer)
        if not res:
            return notes
        WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(expected_conditions.title_contains('Customers Management'))
        if not self.check_if_customer_added(customer):
            notes.append('Customer does not appear in table')
            return notes
        notes.append('Customer Added Successfully')
        return notes

    def delete_customer(self, customer) -> str:
        """
        delete customer.
        by a given customer properties, search him in the
        table and delete it
        :param customer:
        :return:
        """
        flag = False    # flag that indicated if we deleted the element or just didnt find it
        path1 = "//td[contains(text(), '" + customer.first_name + "')]"
        path2 = "//td[contains(text(), '" + customer.last_name + "')]"
        path3 = "//td/a[contains(text(), '" + customer.email + "')]"
        i = 1           # starting with page 1
        while i < NUMBER_OF_PAGES:
            elements_in_table = self.driver.find_elements_by_xpath("//tbody/tr")
            for element in elements_in_table:
                if self._is_x_exist(path1, element) and self._is_x_exist(path2, element) and self._is_x_exist(path3, element):
                    element.find_element_by_xpath("//td/span/a[@title='DELETE']").click()
                    wait = WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD)
                    wait.until(expected_conditions.alert_is_present())
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    flag = True
                    break
            if flag:
                break
            i += 1
            self.driver.find_element_by_xpath("//li/a[text()='{}']".format(i)).click()
            WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(expected_conditions.title_contains('Customers Management'))
        return 'Success' if flag else 'Fail'

    def _is_x_exist(self, path, driver=None) -> bool:
        """
        is_x_path method.
        check if xpath expression is exist. if it doesnt find it, it raises execpetion
        and it will return false.
        :param path:
        :param driver: point where we search for descendant elements
        :return: true if xpath exist else false
        """
        try:
            driver = self.driver if driver is None else driver
            driver.find_element_by_xpath(path)
        except Exception as e:
            print(e)
            return False
        return True

    def check_if_customer_added(self, customer) -> bool:
        """
        check_if_customer_added method.
        check if the customer that we just added appears in the
        table.
        :param customer:
        :return: true if appears else false
        """
        path_first_name = "//tr/td[text()='"+str(customer.first_name)+"']"
        path_last_name = "//tr/td[text()='"+str(customer.last_name)+"']"
        path_mail = "//tr/td/a[text()='" + str(customer.email) + "']"
        return self._is_x_exist(path_first_name) and self._is_x_exist(path_last_name) and self._is_x_exist(path_mail)

    def navigate_to_customers_addition(self):
        """
        navigate_to_customers_addition method.
        navigate to the page of adding customer.
        :return: nothing
        """
        accounts_section_path = "//div[@class='menu-content']/ul/li/a[contains(text(), ' Accounts')]"
        self.driver.find_element_by_xpath(accounts_section_path).click()
        customers_section_path = "//div[@class='menu-content']/ul/li/ul/li/a[starts-with(text(), 'Customers')]"
        self.driver.find_element_by_xpath(customers_section_path).click()

    def entry(self):
        """
        entry method.
        enter to the main menu with the correct username and password.
        :return:
        """
        self.driver.get("https://www.phptravels.net/admin")
        self.driver.find_element_by_name('email').send_keys('admin@phptravels.com')
        self.driver.find_element_by_name('password').send_keys('demoadmin')
        self.driver.find_element_by_css_selector('button').click()
        WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(expected_conditions.title_contains('Dashboard'))

    def add_customer(self, customer) -> (bool, list):
        """
        add_customer method.
        add a customer to table.
        :param customer:
        :return:
        """
        add_button_path = "//div/form/button[contains(text(), 'Add')]"
        self.driver.find_element_by_xpath(add_button_path).click()
        self.driver.find_element_by_xpath("//input[@name='address1']").send_keys(customer.address_1)
        self.driver.find_element_by_xpath("//input[@name='address2']").send_keys(customer.address_2)
        elements = self.driver.find_element_by_xpath("//div[@class ='panel-body']")
        self._fill_fields(elements, customer)
        self.driver.find_element_by_css_selector('button').click()
        try:
            WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(
                expected_conditions.title_contains("Customers Management"))
        except Exception:
            return False, self._check_reason_of_fail()
        return True, []

    def _check_reason_of_fail(self) -> list:
        """
        check_reason_of_fail method.
        retrieve the reasons which the addition of customer failed and return
        it in a list
        :return: list of warnings
        """
        str_alerts = []
        alerts = self.driver.find_elements_by_xpath("//div[@class='alert alert-danger']/p")
        for alert in alerts:
            str_alerts.append(alert.text)
        return str_alerts

    def _fill_fields(self, elements, customer):
        """
        _fill_fields method.
        fill the form of Add Customer with his propperties
        :param elements: list of forms
        :param customer: customer
        :return: void
        """
        list_of_forms = elements.find_elements_by_xpath("//div/div/input")
        country_option_path = "//select[@name='country']/option[text()='" + str(customer.country) + "']"
        list_of_forms[COUNTRY].find_element_by_xpath(country_option_path).click()
        customer_status_path = "//select[@name='status']/option[text()='" + str(customer.status) + "']"
        list_of_forms[STATUS].find_element_by_xpath(customer_status_path).click()
        list_of_forms[FIRST_NAME].send_keys(customer.first_name)
        list_of_forms[LAST_NAME].send_keys(customer.last_name)
        list_of_forms[EMAIL].send_keys(customer.email)
        list_of_forms[PASSWORD].send_keys(customer.password)
        list_of_forms[MOBILE].send_keys(customer.mobile)

    def sign_out(self):
        """
        sign_out method.
        sign out from the menu, and if from some reason it doesnt log out -> raises exception
        :return: void
        """
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log Out')]").click()
        WebDriverWait(self.driver, TIME_WAIT_FOR_PAGE_LOAD).until(expected_conditions.title_contains('Administator Login'))

    def shutdown_driver(self):
        """
        shutdown_driver method.
        close the driver
        :return: void
        """
        self.driver.close()



# add const defines - V
# add shemot mashumautiem - V
# add type annoatios - V
# doc string below the methods
# pass on every line and see what he does
# self.driver....
# _private - V
# pass e of execeptiion
# methods name represent what need to be not waht actually
# remove finally - V