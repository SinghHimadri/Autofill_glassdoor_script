# region IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
# region END


# dictionary of user's preferenes
# make changes here
CHOICES = {
    "job_title": "Software Engineer",
    "location": "Pune (India)"
}


# opens glassdoor website and waits until user login
def glassdoor_config(driver):

    driver.get('https://www.glassdoor.com/index.htm')

    # keep waiting for user to log-in until the URL changes to user page
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_contains("change"))
        except TimeoutException:
            break
    return True


# fill entries and search jobs
def search_job(driver):

    # wait until search bar to appears
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='scBar']"))
        )

    try:
        # locating company and location bar
        company_field = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        location_field = driver.find_element_by_xpath("//*[@id='sc.location']")
        company_field.clear()
        location_field.clear()

        # filling user's choice
        company_field.clear()
        company_field.send_keys(CHOICES['job_title'])
        location_field.clear()
        location_field.send_keys(CHOICES['location'])

        # clicking search bar
        time.sleep(1)
        driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()

        # close a random popup if it shows up
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass

        return True

    except NoSuchElementException:
        return False


def getURLs():

    driver = webdriver.Chrome(ChromeDriverManager().install())
    success = glassdoor_config(driver)
    if not success:
        # improvement required
        driver.close()

    success = search_job(driver)
    if not success:
        driver.close()


if __name__ == '__main__':
    getURLs()
