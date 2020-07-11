#region IMPORTS
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

# Lever Application form
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

    # university(if asked)
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(INFORMATION['university']) # find university in dropdown
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