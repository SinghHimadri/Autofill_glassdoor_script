# egion IMPORTS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os
import time
import job_list
# region END


# Fill your personal details
INFORMATION = {
    "first_name": "Foo",
    "last_name": "Bar",
    "email": "eg@eg.com",
    "phone": "1234567",
    "org": "Self-Employed",
    "resume": "resume.pdf",
    "resume_textfile": "resume_short.txt",
    "linkedin": "https://www.linkedin.com/",
    "website": "www.youtube.com",
    "github": "https://github.com",
    "twitter": "www.twitter.com",
    "location": "ABC, XYZ",
    "grad_month": '06',
    "grad_year": '2021',
    "university": "IIIT"
}


# Parsing Lever Application form
def lever(driver):

    # Open the application web page
    driver.find_element_by_class_name('template-btn-submit').click()

    # Fill Personals
    first_name = INFORMATION['first_name']
    last_name = INFORMATION['last_name']
    full_name = first_name + ' ' + last_name
    driver.find_element_by_name('name').send_keys(full_name)
    driver.find_element_by_name('email').send_keys(INFORMATION['email'])
    driver.find_element_by_name('phone').send_keys(INFORMATION['phone'])
    driver.find_element_by_name('org').send_keys(INFORMATION['org'])

    # socials
    driver.find_element_by_name('urls[LinkedIn]').send_keys(INFORMATION['linkedin'])
    driver.find_element_by_name('urls[Twitter]').send_keys(INFORMATION['twitter'])

    try:
        driver.find_element_by_name('urls[Github]').send_keys(INFORMATION['github'])
    except NoSuchElementException:
        try:
            driver.find_element_by_name('urls[GitHub]').send_keys(INFORMATION['github'])
        except NoSuchElementException:
            pass
    driver.find_element_by_name('urls[Portfolio]').send_keys(INFORMATION['website'])

    # University(if asked)
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(INFORMATION['university'])  # find university in dropdown
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass

    # add how you found out about the company
    try:
        driver.find_element_by_class_name('application-dropdown').click()
        search = driver.find_element_by_xpath("//select/option[text()='Glassdoor']").click()
    except NoSuchElementException:
        pass

    # Resume clickable file-upload
    driver.find_element_by_name('resume').send_keys(os.getcwd()+"/resume.pdf")
    driver.find_element_by_class_name('template-btn-submit').click()


# Parsing Greenhouse application form
def greenhouse(driver):

    # basic info
    driver.find_element_by_id('first_name').send_keys(INFORMATION['first_name'])
    driver.find_element_by_id('last_name').send_keys(INFORMATION['last_name'])
    driver.find_element_by_id('email').send_keys(INFORMATION['email'])
    driver.find_element_by_id('phone').send_keys(INFORMATION['phone'])

    # If doesn't works user has to complete the action
    try:
        loc = driver.find_element_by_id('job_application_location')
        loc.send_keys(INFORMATION['location'])
        loc.send_keys(Keys.DOWN) # manipulate a dropdown menu
        loc.send_keys(Keys.DOWN)
        loc.send_keys(Keys.RETURN)
        time.sleep(2) # give user time to manually input if this fails

    except NoSuchElementException:
        pass

    # Upload Resume as a Text File in Resume paste option
    driver.find_element_by_css_selector("[data-source='paste']").click()
    resume_zone = driver.find_element_by_id('resume_text')
    resume_zone.click()
    with open(INFORMATION['resume_textfile']) as f:
        lines = f.readlines() # add each line of resume to the text area
        for line in lines:
            resume_zone.send_keys(line.decode('utf-8'))

    # linkedin
    try:
        driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]").send_keys(INFORMATION['linkedin'])
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath("//label[contains(.,'Linkedin')]").send_keys(INFORMATION['linkedin'])
        except NoSuchElementException:
            pass
# User to make changes here for drop down menu
    # graduation year
    try:
        driver.find_element_by_xpath("//select/option[text()='2021']").click()
    except NoSuchElementException:
        pass

    # university
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Harvard')]").click()
    except NoSuchElementException:
        pass

    # degree
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Bachelor')]").click()
    except NoSuchElementException:
        pass

    # major
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Computer Science')]").click()
    except NoSuchElementException:
        pass

    # website
    try:
        driver.find_element_by_xpath("//label[contains(.,'Website')]").send_keys(INFORMATION['website'])
    except NoSuchElementException:
        pass

    # work authorization
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'any employer')]").click()
    except NoSuchElementException:
        pass

    driver.find_element_by_id("submit_app").click()


# main
if __name__ == '__main__':

    # scrape job listings from glassdoor
    aggregatedURLs = job_list.getURLs()
    print(f'Job Listings: {aggregatedURLs}')
    print('\n')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    for url in aggregatedURLs:
        print('\n')

        if 'greenhouse' in url:
            driver.get(url)
            try:
                greenhouse(driver)
                print(f'SUCCESS FOR: {url}')
            except Exception:
                # print(f"FAILED FOR {url}")
                continue

        elif 'lever' in url:
            driver.get(url)
            try:
                lever(driver)
                print(f'SUCCESS FOR: {url}')
            except Exception:
                # print(f"FAILED FOR {url}")
                continue
        else:
            # print(f"NOT A VALID APP LINK FOR {url}")
            continue

        time.sleep(2)

    driver.close()
