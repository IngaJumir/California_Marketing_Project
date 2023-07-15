from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from threading import Thread
from inga import my_key
import Helpers as H
from faker import Faker

fake = Faker()

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or my_key.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or my_key.BROWSERSTACK_ACCESS_KEY
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "browserstack-Cross-Browser-test"
capabilities = [
    {
        "browserName": "chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "BStack Python sample parallel-Chrome-Win10",
        "buildName": BUILD_NAME,
    },
    {
        "browserName": "firefox",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack Python sample parallel-Firefox-Win10",
        "buildName": BUILD_NAME,
    },
    {
        "browserName": "safari",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Big Sur",
        "sessionName": "BStack Python sample parallel-Safari-BigSur",
        "buildName": BUILD_NAME,
    },
    {
        "browserName": "safari",
        "browserVersion": "14.1",
        "os": "OS X",
        "osVersion": "Big Sur",
        "sessionName": "BStack Python sample parallel-Safari-BigSur",
        "buildName": BUILD_NAME,
    },
]


def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())


def run_session(cap):
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
    try:
        # test1 Chrome
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 2 - Sign-up on website  (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Verify that Main log in is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.m_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.m_login)))
        time.sleep(7)
        driver.find_element(By.XPATH, H.m_login).click()
        H.delay()

        # Verify that button "Sign Up With Email" is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.sign_up_with_email)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.sign_up_with_email)))
        driver.find_element(By.XPATH, H.sign_up_with_email).click()

        # Fill in the sign-up form with fake credentials(Helpers)
        fakeEmail = fake.email()

        email_field = driver.find_element(By.XPATH, H.e_signup)
        email_field.clear()
        email_field.send_keys(fakeEmail)

        password_field = driver.find_element(By.XPATH, H.p_signup)
        password_field.clear()
        password_field.send_keys(H.fakePassword)

        # Submit the sign-up form
        signup_button = driver.find_element(By.XPATH, H.signup_btn)
        signup_button.click()

        time.sleep(6)

        # Extract the name from the email address
        name = fakeEmail.split('@')[0]

        # Construct the expected account text
        expected_account_text = f"Hello {name}"

        # Retrieve the text on the account page
        account_text_element = driver.find_element(By.XPATH, "//div[@class='dI69aw']")
        account_text = account_text_element.text

        # Assert that the expected account text is present in the retrieved text
        try:
            assert expected_account_text in account_text
            print(
                f"User successfully signed up and directed to their account. Expected account text: {expected_account_text}")
        except AssertionError:
            print("User sign-up failed or not directed to the account")
    finally:
        driver.quit()


for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()