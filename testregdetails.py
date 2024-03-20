#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sys
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#-----------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Test the ability of the reg application to '
            + 'handle "secondary" (class details) queries')

    parser.add_argument(
        'serverURL', metavar='serverURL', type=str,
        help='the URL of the reg application')

    parser.add_argument(
        'mode', metavar='mode', type=str,
        choices=['normal','headless'],
        help='the mode (normal or headless) that this program should '
            + 'use when interacting with Firefox; headless tells '
            + 'Firefox not to display its window and so is faster, '
            + 'especially when using X Windows')

    args = parser.parse_args()

    return (args.serverURL, args.mode)

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_test(server_url, driver, classid):

    print_flush('-----------------')
    print_flush('classid: ' + classid)
    try:
        driver.get(server_url)
        link_element = driver.find_element(By.LINK_TEXT, classid)
        link_element.click()
        class_details_table = driver.find_element(
            By.ID, 'classDetailsTable')
        print_flush(class_details_table.text)
        course_details_table = driver.find_element(
            By.ID, 'courseDetailsTable')
        print_flush(course_details_table.text)
    except Exception as ex:
        print(str(ex))

#-----------------------------------------------------------------------

def main():

    server_url, mode = get_args()

    if mode == 'normal':
        driver = webdriver.Firefox()
    else:
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

    run_test(server_url, driver, '8321')
    run_test(server_url, driver, '9032')

    # Add more tests here.

    driver.quit()

if __name__ == '__main__':
    main()
