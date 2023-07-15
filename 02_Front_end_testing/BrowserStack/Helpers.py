from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
from faker import Faker

fake = Faker()

# Website URL
QASV_URL = "https://qasvus.wixsite.com/ca-marketing"

# Main logo
Page_logo = "//img[@alt='iot_sq.png']"


# Sign-up
m_login = "//span[contains(text(),'Log In')]"
sign_up_with_email = "//span[normalize-space()='Sign up with email']"
signup_btn = "//span[contains(text(),'Sign Up')]"

# Email field for sign up
e_signup = "//input[@id='input_input_emailInput_SM_ROOT_COMP747']"
# Password field for sign up
p_signup = "//input[@id='input_input_passwordInput_SM_ROOT_COMP747']"

# Fake credentials
fakeEmail = fake.email()
fakePassword = fake.password()

# Assert title
def assert_title(driver, expected_title):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_is(expected_title))

    actual_title = driver.title
    if expected_title in actual_title:
        print(f"Page has '{actual_title}' as the expected title")
    else:
        screenshot_path = f"Page_has_different_{expected_title}.png"
        driver.save_screenshot(screenshot_path)
        raise AssertionError(f"Page has '{actual_title}' instead of the expected title '{expected_title}'."
                             f" Screenshot saved as '{screenshot_path}'")



# Check API response code
def check_API_code(driver):
    response = requests.get(driver.current_url)
    code = response.status_code
    if code == 200:
        print(f"API response code for URL '{driver.current_url}' is {code}")
    else:
        print(f"API response code for URL '{driver.current_url}' is not 200, current code is {code}")


def delay():
    time.sleep(random.randint(1, 3))



