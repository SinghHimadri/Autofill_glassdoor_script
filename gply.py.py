# region IMPORTS
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# end region


# opens glassdoor website and waits until user login
def glassdoor_config(driver):

    driver.get('https://www.glassdoor.co.in/index.htm')

    # keep waiting for user to log-in until the URL changes to user page
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_changes("change"))
        except TimeoutException:
            break
    return True


# fill entries and search jobs 
def search_job(driver):

    




def start():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    glassdoor_config(driver)
    
start()