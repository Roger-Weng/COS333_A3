#-----------------------------------------------------------------------
# testreg.py
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
            + 'handle "primary" (class overviews) queries')

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

def run_test(driver, input_values):

    print_flush('-----------------')
    for key, value in input_values.items():
        print_flush(key + ': |' + value + '|')

    try:
        if 'dept' in input_values:
            dept_input = driver.find_element(By.ID, 'deptInput')
            dept_input.send_keys(input_values['dept'])
        if 'coursenum' in input_values:
            coursenum_input = driver.find_element(By.ID,
                'coursenumInput')
            coursenum_input.send_keys(input_values['coursenum'])
        if 'area' in input_values:
            area_input = driver.find_element(By.ID, 'areaInput')
            area_input.send_keys(input_values['area'])
        if 'title' in input_values:
            title_input = driver.find_element(By.ID, 'titleInput')
            title_input.send_keys(input_values['title'])

        submit_button = driver.find_element(By.ID, 'submitButton')
        submit_button.click()

        overviews_table = driver.find_element(By.ID, 'overviewsTable')
        print_flush(overviews_table.text)

        if 'dept' in input_values:
            dept_input = driver.find_element(By.ID, 'deptInput')
            dept_input.clear()
        if 'coursenum' in input_values:
            coursenum_input = driver.find_element(By.ID,
                'coursenumInput')
            coursenum_input.clear()
        if 'area' in input_values:
            area_input = driver.find_element(By.ID, 'areaInput')
            area_input.clear()
        if 'title' in input_values:
            title_input = driver.find_element(By.ID, 'titleInput')
            title_input.clear()
    except Exception as ex:
        print(str(ex), file=sys.stderr)

#-----------------------------------------------------------------------

def main():

    server_url, mode = get_args()

    if mode == 'normal':
        driver = webdriver.Firefox()
    else:
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

    driver.get(server_url)

    run_test(driver, {'dept':'COS'})
    run_test(driver,
        {'dept':'COS', 'coursenum':'2', 'area':'qr', 'title':'intro'})

    # Add more tests here.

    driver.quit()

if __name__ == '__main__':
    main()
