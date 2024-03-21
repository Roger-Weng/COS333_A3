#-----------------------------------------------------------------------
# testreg.py
# Authors: Roger Weng, Vishva Ilavelan
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

    run_test(driver, {})
    run_test(driver, {'coursenum': "333"})
    run_test(driver, {'coursenum': "b"})
    run_test(driver, {'area': "qr"})
    run_test(driver, {'title': "intro"})
    run_test(driver, {'title': "science"})
    run_test(driver, {'title': "c%S"})
    run_test(driver, {'title': "c_S"})
    run_test(driver, {'title': "c\%s"})
    run_test(driver, {'dept': "cos", 'coursenum': "3"})
    run_test(driver, {'title': "Independent Study"})
    run_test(driver, {'title': "Independent Study "})
    run_test(driver, {'title': "Independent Study  "})
    run_test(driver, {'title': " Independent Study"})
    run_test(driver, {'title': "  Independent Study"})
    run_test(driver, {"title": "=-c"})
    run_test(driver, {"title": "-c"})

    # test injection
    run_test(driver, {"dept": "junk' OR 'x'='x"})
    run_test(driver, {"area": "junk' OR 'x'='x"})
    run_test(driver, {"title": "junk' OR 'x'='x"})
    run_test(driver, {"coursenum": "junk' OR 'x'='x"})
    run_test(driver, {"dept": "junk' OR 'x'='x", "coursenum": "junk' OR 'x'='x",
                      "title": "junk' OR 'x'='x", "area": "junk' OR 'x'='x"})
    
    run_test(driver, {"dept": "", "coursenum": "", "title": "", "area": ""})
    run_test(driver, {"dept": " ", "coursenum": " ", "title": " ", "area": " "})
    run_test(driver, {"dept": "  ", "coursenum": "  ", "title": "  ", "area": "  "})
    run_test(driver, {"title": "", "area": "S"})
    run_test(driver, {"dept": "c"})
    run_test(driver, {"title": "p"})
    run_test(driver, {"coursenum": "0"})
    run_test(driver, {"area": "c"})

    # testing where all flags are used with input

    run_test(driver, {"title": "the", "area": "sa", "coursenum": "21", "dept": "e"})

    # test each search parameter / flag individually

    run_test(driver, {"title": "systems"})
    run_test(driver, {"area": "qr"})
    run_test(driver, {"dept": "phy"})
    run_test(driver, {"coursenum": "104"})

    # unusual searches

    run_test(driver, {"title": "-"})
    run_test(driver, {"title": '";''"&'})
    run_test(driver, {"title": "&"})
    run_test(driver, {"title": "?"})
    run_test(driver, {"title": " %%%%'____-%%%%__'"})
    run_test(driver, {"title":  "'%_%_%_%%%%%%___%%_%__%'"})
    
    # full search 


    run_test(driver, {"dept": "FRS", "coursenum": "178", "title": "Modern Financial Markets", "area": "SA"})
    run_test(driver, {"dept": "WWS", "coursenum": "556B", "title": "Topics in International Relations: International Justice"})
    run_test(driver, {"dept": "ORF", "coursenum": "527", "title": 'Stochastic Calculus and Finance'})
    run_test(driver, {"dept": "MAT", "coursenum": "203", "title": 'Advanced Multivariable Calculus', "area": "QR"})

    # test corner cases associated with escaping 

    run_test(driver, {"title": "-t \\casf\\l\\jkwefj \\eere"})
    run_test(driver, {"title": "\\"""})
    run_test(driver, {"title": "t\h\e"})
    run_test(driver, {"title": "t\\h\\e"})
    run_test(driver, {"title": "t\\\h\\\e"})
    run_test(driver, {"title": "t\\\\h\\\\e"})

    run_test(driver, {"dept": "COS"})
    run_test(driver, {"coursenum": "1"})
    run_test(driver, {"area": "QR"})

    run_test(driver, {"area": "h", "dept": "c", "coursenum": "2", "title": "h"})
    
    # one each

    run_test(driver, {"dept": "MAT"})
    run_test(driver, {"coursenum": "10"})
    run_test(driver, {"title": "-"})
    run_test(driver, {"area": "a", "title": "t"})
    run_test(driver, {"coursenum": "0", "dept": "his", "title": "roman"})

    driver.quit()

if __name__ == '__main__':
    main()
