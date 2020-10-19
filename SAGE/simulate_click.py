from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def download_pdf(url):

    browser = webdriver.Chrome()

    try:
        browser.get(url)

        action = ActionChains(browser)

        action.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        action.key_down(Keys.ENTER).send_keys('s').key_up(Keys.ENTER).perform()

    finally:
        browser.close()


if __name__ == "__main__":
    download_pdf("http://sage.cnpereading.com/paragraph/download/?doi=10.2307/2667000")
