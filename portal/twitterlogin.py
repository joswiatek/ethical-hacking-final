import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import time
import os

"""
TEST ACCOUNT
user: myname69323307
password: peanutbutter
"""

usr = raw_input('Enter your username or email: ')
pwd = getpass('Enter your password : ')
url = 'https://www.twitter.com/login'


def loginTwitter(username, password):
    cwd = os.getcwd()

    browser = selenium.webdriver.Chrome(cwd + '/chromedriver')
    browser.get(url)
    fillusr = browser.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input')
    fillusr.send_keys(username)
    fillpass = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')))
    fillpass.send_keys(password)
    login = browser.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
    login.click()

    # Wait for page to load
    time.sleep(5)

    # Write our tweet
    content = browser.find_element_by_id('tweet-box-home-timeline')
    # ...you might have to do this twice if it doesn't respond right away
    content.send_keys("""I just got pwned by a fake captive portal! Don't reuse your credentials!""")

    #"""
    # Try to attach an image.

    img_path = cwd + "/pwned.jpg"

    # Attach an image
    browser.find_element_by_css_selector('input.file-input').send_keys(img_path)
    #WebDriverWait(browser, 5).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.js-show-preview'))
    #)
    #"""

    # Wait for image to upload
    time.sleep(5)

    # Submit the tweet
    browser.find_element_by_css_selector('button.tweet-action').click()

loginTwitter(usr, pwd)
time.sleep(5)
