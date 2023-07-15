from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
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

# Menu buttons
Home_menu = "//p[@id='comp-ldaaacya0label']"
Blog_menu = "//p[@id='comp-ldaaacya1label']"
Shop_menu = "//p[@id='comp-ldaaacya2label']"
Services_menu = "//p[@id='comp-ldaaacya3label']"

# Sign-up
m_login = "//span[contains(text(),'Log In')]"
sign_up_with_email = "//span[normalize-space()='Sign up with email']"
signup_btn = "//span[contains(text(),'Sign Up')]"

# Email field for sign up
e_signup = "//input[@id='input_input_emailInput_SM_ROOT_COMP747']"
# Password field for sign up
p_signup = "//input[@id='input_input_passwordInput_SM_ROOT_COMP747']"

# Log in
main_login = "//span[contains(text(),'Log In')]"
inner_login = "//button[contains(text(),'Log In')]"
login_with_email = "//span[contains(text(),'Log in with Email')]"
last_login = "//span[@class='M3I7Z2 wixui-button__label'][normalize-space()='Log In']"

# Email field for sign in
e_signin = "//input[@id='input_input_emailInput_SM_ROOT_COMP748']"
# Password field for sign in
p_signin = "//input[@id='input_input_passwordInput_SM_ROOT_COMP748']"

# Fake credentials
fakeEmail = fake.email()
fakePassword = fake.password()
fakeName = fake.name()

# Social Media "Vk"
vk = "//wow-image[@id='img_2_comp-ldaaabc9']//img[@alt='VK Share']"
vk_URL = "https://vk.com/qa_at_silicon_valley"
vk_Title = "QA at Silicon Valley California | VK"
vk_logo = "//*[name()='path' and contains(@d,'M15.96 21.')]"
vk_follow = "//span[@class='FlatButton__content'][normalize-space()='Follow']"

# Shopping menu
shop_button = "//p[@id='comp-ldaaacya2label']"
product_6_button = "//span[normalize-space()='$40.00']"
product_color = ".RadioButton330525410__root:nth-child(2) .ColorPickerItem2577026692__radioInner"
cart_button = "//span[contains(text(),'Add to Card')]"
def_quantity = "//input[contains(@type,'number')]"
view_cart = "//*[name()='text' and contains(@class,'bGBBgJ jDu')]"
view_cart_btn = "//a[@id='widget-view-cart-button']"
product_11 = "//span[normalize-space()='Sale']"
quantity_def = "//input[@value='1']"
quantity_field = "//input[contains(@type,'number')]"

# Connect with us form
connect_w_us = "//span[contains(text(),'CONECT WIT USS')]"
name_field = "//input[@id='input_comp-k00d77t1']"
email_field = "//input[@id='input_comp-k00d77ti']"
subject_field = "//input[@id='input_comp-k00d77tz']"
message_field = "//textarea[@id='textarea_comp-k00d77uc']"
submit_form = "//div[@id='comp-k00d77uq']//button[@class='kuTaGy wixui-button zKbzSQ']"

# Event menu
event_menu = '//*[@class="tfCiE0"]'
event_2 = '//a[@href= "https://qasvus.wixsite.com/ca-marketing/event-info/event-2-3"]'
location = "//p[@data-hook='event-full-location']"
date = "//p[contains(text(),'Jan 09, 2025, 11:30 AM')]"
rsvp_btn = "//button[@class='cZcLi2 IikhGe']"
first_name = "//input[@id='firstName']"
last_name = "//input[@id='lastName']"
e_email = "//input[@id='email']"
submit = "//button[normalize-space()='SUBMIT']"


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


# Check if logo is present
def check_logo_presence(driver, locator):
    try:
        driver.find_element(*locator)
        print("Logo is present on the page")
    except NoSuchElementException:
        print("Logo not found:", locator)


# Scrolling to element
def scroll_to_element(driver, element_xpath):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except NoSuchElementException:
        print(f"Element '{element_xpath}' not found for scrolling")


# Verify Checkout
def checkout_product(driver):
    try:
        wait = WebDriverWait(driver, 10)
        # Verify that Element Photo is Visible
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-hook="product-thumbnail-media"]')))
        # Verify that Logo is visible
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@alt="iot_sq.png"]')))
        # verify button "Checkout"
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Checkout']")))
        # Checkout button is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Checkout']")))
        # Click on Checkout that verify order is placed
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Checkout']"))).click()
        print("All Elements are present and 'Checkout' button is OK")
    except NoSuchElementException:
        print("One of El is missed and Checkout is impossible!")


# Assert error message
def verify_error_message(driver):
    try:
        wait = WebDriverWait(driver, 3)
        error_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"We can\'t '
                                                                               'accept online orders right now")]')))
        # Retrieve the text content of the element
        error_text = error_element.text
        print(error_text)

        # Assert that the expected error message is present in the text
        assert "We can't accept online orders right now" in error_text
    except TimeoutException:
        print("Error message verification failed")


# Check visibility and click ability of the main page menu
def check_menu_visibility_and_clickable(driver, locator):
    wait = WebDriverWait(driver, 3)
    wait.until(EC.visibility_of_element_located(locator))
    wait.until(EC.element_to_be_clickable(locator))
    locator_xpath = locator[1]
    menu_name = menu_mapping.get(locator_xpath, locator_xpath)
    print(f"{menu_name} menu is visible and clickable")


menu_mapping = {
    "//p[@id='comp-ldaaacya0label']": "Home_menu",
    "//p[@id='comp-ldaaacya1label']": "Blog_menu",
    "//p[@id='comp-ldaaacya2label']": "Shop_menu",
    "//p[@id='comp-ldaaacya3label']": "Services_menu",
}


def delay():
    time.sleep(random.randint(1, 3))
