# region IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import urllib.request
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
            WebDriverWait(driver, 1).until(EC.url_contains("member"))
        except TimeoutException:
            break
    return True


# fill entries and search jobs
def search_job(driver):

    # wait until search bar to appears
    WebDriverWait(driver, 20).until(
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


# get all jobs url links set
def aggregate_links(driver):
    allLinks = [] 

    # wait for page to fully load
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
        )

    time.sleep(5)

    # parse the page source using beautiful soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)

    # find all hrefs
    allJobLinks = soup.findAll("a", {"class": "jobLink"})
    allLinks = [jobLink['href'] for jobLink in allJobLinks]
    allFixedLinks = []

    # clean up the job links by opening, modifying, and 'unraveling' the URL
    for link in allLinks:
        # first, replace GD_JOB_AD with GD_JOB_VIEW
        # this will replace the Glassdoor hosted job page to the proper job page
        # hosted on most likely Greenhouse or Lever
        link = link.replace("GD_JOB_AD", "GD_JOB_VIEW")

        # if there is no glassdoor prefex, add that
        # for example, /partner/jobListing.htm?pos=121... needs the prefix

        if link[0] == '/':
            link = f"https://www.glassdoor.com{link}"

        # then, open up each url and save the result url
        # because we got a 403 error when opening this normally, we have to establish the user agent
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,}
        request=urllib.request.Request(link,None,headers) #The assembled request

        try:
            # the url is on glassdoor itself, but once it's opened, it redirects - so let's store that
            response = urllib.request.urlopen(request)
            newLink = response.geturl()

            # if the result url is from glassdoor, it's an 'easy apply' one and worth not saving
            # however, this logic can be changed if you want to keep those
            if "glassdoor" not in newLink:
                print(newLink)
                print('\n')
                allFixedLinks.append(newLink)
        except Exception:
            # horrible way to catch errors but this doesnt happen regualrly (just 302 HTTP error)
            print(f'ERROR: failed for {link}')
            print('\n')

    # convert to a set to eliminate duplicates
    return set(allFixedLinks)


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
