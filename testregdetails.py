#-----------------------------------------------------------------------
# testregdetails.py
# Authors: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------

import sys
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sqlite3
import contextlib

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def getclassids(): 
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT classid "
                stmt_str += "FROM classes "
                cursor.execute(stmt_str)
                table = cursor.fetchall()
                return table      
            
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

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

    run_test(server_url, driver, '  9032')
    run_test(server_url, driver, '9032   ')
    run_test(server_url, driver, '  8321  ')
    run_test(server_url, driver, 'aksdfjlka')
    run_test(server_url, driver, ' dsf 9032')
    run_test(server_url, driver, '')
    run_test(server_url, driver, "7899")
    run_test(server_url, driver, "7909")
    run_test(server_url, driver, "8038")
    run_test(server_url, driver, "10022")
    run_test(server_url, driver, "8069")
    run_test(server_url, driver, "8038")
    run_test(server_url, driver, "8019")
    run_test(server_url, driver, "8012")
    run_test(server_url, driver, "7959")
    run_test(server_url, driver, "8755")
    run_test(server_url, driver, "8381")
    run_test(server_url, driver, '8253')
    num = 9177
    run_test(server_url, driver, num)
    run_test(server_url, driver, "9014")



if __name__ == '__main__':
    main()
