from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def glassdoor_config(driver):
    driver.get('https://www.glassdoor.co.in/index.htm')
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_changes("change"))
        except TimeoutException:
            break
    return True

def start():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    glassdoor_config(driver)
    
start()