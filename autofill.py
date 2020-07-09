from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os 
import time
import job_list


if __name__ == '__main__':

    # call get_links to automatically scrape job listings from glassdoor
    aggregatedURLs = job_list.getURLs()
    print(f'Job Listings: {aggregatedURLs}')
    print('\n')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    for url in aggregatedURLs:
        print('\n')
    driver.close()