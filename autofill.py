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