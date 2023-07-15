from selenium import webdriver
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import random
import time
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.edge.service import Service
import Helpers as H
from faker import Faker

fake = Faker()


class chrome_California_Marketing(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def test_chrome_verify_website_link(self):
        driver = self.driver
        # Open URL - home page
        driver.get(H.QASV_URL)
        driver.maximize_window()
        # Set another Window Size
        # driver.set_window_size(1200, 800)

        print("Positive_Test")
        print("TEST 1 - Verify Website Link  (Chrome Browser) \n")

        # Check API Response Code
        print("California Marketing Url has", requests.get(H.QASV_URL).status_code, "as status Code")
        code = requests.get(H.QASV_URL).status_code
        if code == 200:
            print("API response code is OK")
        else:
            print("API response code is not 200", "Current code is:", code)

        # Check Title is correct
        try:
            assert "Home | California Marcketing" in driver.title
        except AssertionError:
            print("Driver title in Chrome is:", driver.title)

        # Check that the LOGO is present
        H.check_logo_presence(driver, (By.XPATH, H.Page_logo))

        # Check "California Marketing" page functionality
        wait = WebDriverWait(driver, 3)

        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Home_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Blog_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Shop_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Services_menu))

    def test_chrome_Sign_Up(self):
        driver = self.driver
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

    def test_chrome_Sign_In(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 3 - Verify login with valid username and password  (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        time.sleep(4)

        # Verify that Main log in is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.main_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.main_login)))
        driver.find_element(By.XPATH, H.main_login).click()
        H.delay()

        # Switch from 'Sign Up' to 'Log In'
        wait.until(EC.visibility_of_element_located((By.XPATH, H.inner_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.inner_login)))
        driver.find_element(By.XPATH, H.inner_login).click()

        # Set wait until button 'Log In with Email' will be visible and click on it
        wait.until(EC.visibility_of_element_located((By.XPATH, H.login_with_email)))
        driver.find_element(By.XPATH, H.login_with_email).click()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.e_signin).clear()
        driver.find_element(By.XPATH, H.e_signin).send_keys(H.fakeEmail)
        driver.find_element(By.XPATH, H.e_signin).click()

        # Clear fields and type user's password
        driver.find_element(By.XPATH, H.p_signin).clear()
        driver.find_element(By.XPATH, H.p_signin).send_keys(H.fakePassword)
        driver.find_element(By.XPATH, H.p_signin).click()

        # Verify Final Log is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.last_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.last_login)))

        # Click on The button "Log In"
        driver.find_element(By.XPATH, H.last_login).click()
        time.sleep(10)

    def test_chrome_Vk_link(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 4 - Validate Vk linked icon leads to correct page   (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Validate Vk linked icon leads to correct page:
        try:
            driver.find_element(By.XPATH, H.vk).click()
            print("Vk icon is clickable")
        except NoSuchElementException:
            print("Vk icon is NOT clickable")

        driver.switch_to.window(driver.window_handles[-1])

        # Verify correct Social media page was reached by URL:
        vkURL = driver.current_url
        if vkURL == H.vk_URL:
            print("Current Vk URL is correct:", driver.current_url)
        else:
            print("Vk URL is different from expected:", driver.current_url)

        # Verify correct Social media page was reached by Title:
        vk_expected_title = H.vk_Title
        if driver.title == vk_expected_title:
            print("Vk title is correct:", driver.title)
        else:
            print("Vk title is different from expected:", driver.title)

        # Verify correct Social media page was reached by Logo:
        try:
            driver.find_element(By.XPATH, H.vk_logo)
            print("Vk Logo was found")
        except NoSuchElementException:
            print("Vk Logo was not found")

        H.delay()

        # Verify Specific element is present on page:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located((By.XPATH, H.vk_follow)))
        try:
            driver.find_element(By.XPATH, H.vk_follow)
            print("Vk specific element is present on the opened page")
        except NoSuchElementException:
            print("No specific Vk element on the opened page")

        # Make driver back on previous page:
        driver.back()

        # Wait 1-3 sec:
        H.delay()

    def test_chrome_Shopping_Cart(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 5 - Add to shopping cart a product and checkout   (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Locate and Click on Shop menu
        driver.find_element(By.XPATH, H.shop_button).click()

        # Click on product 6 "Blow-drier"
        driver.find_element(By.XPATH, H.product_6_button).click()

        # Verify Quantity, by default is 1
        wait.until(EC.visibility_of_element_located((By.XPATH, H.def_quantity)))

        # Verify that  "Add to Cart" button is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.cart_button)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.cart_button)))
        time.sleep(3)

        # Add product to cart
        driver.find_element(By.XPATH, H.cart_button).click()
        time.sleep(5)

        # Switch to "View Cart" frame
        driver.switch_to.frame(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, H.view_cart_btn)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.view_cart_btn)))
        driver.find_element(By.XPATH, H.view_cart_btn).click()
        # time.sleep(5)

        # Assert Driver Title
        H.assert_title(driver, 'Cart | California Marketing')
        time.sleep(5)

        # Function for Checkout
        H.checkout_product(driver)

        time.sleep(3)

        # Switch to "Checkout" frame
        driver.switch_to.frame(2)

        # Assert that User Cannot place an order
        H.verify_error_message(driver)

        print("Test is 'FAIL' cause user Can't place an order!")

    def test_chrome_ConnectWithUs_form(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 6 - Verify Connect with us form  (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Scroll to "Connect with us" form
        H.scroll_to_element(driver, H.connect_w_us)

        # Assert that the text "CONECT WIT USS" is correct
        text_element = driver.find_element(By.XPATH, H.connect_w_us)
        text = text_element.text
        expected_text = "CONNECT WITH US"

        try:
            assert text == expected_text, f"Text is '{text}', expected '{expected_text}'"
        except AssertionError:
            # Print error message
            print("Assertion failed, text is different than expected")

        # Clear fields and type user's name
        driver.find_element(By.XPATH, H.name_field).clear()
        driver.find_element(By.XPATH, H.name_field).send_keys(H.fakeName)
        H.delay()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.email_field).clear()
        driver.find_element(By.XPATH, H.email_field).send_keys(H.fakeEmail)
        H.delay()

        # Clear fields and type user's subject
        driver.find_element(By.XPATH, H.subject_field).clear()
        driver.find_element(By.XPATH, H.subject_field).send_keys("Job")
        H.delay()

        # Clear fields and type user's message
        driver.find_element(By.XPATH, H.message_field).clear()
        driver.find_element(By.XPATH, H.message_field).send_keys("Hello!")
        H.delay()

        # Submit form
        wait.until(EC.element_to_be_clickable((By.XPATH, H.submit_form)))
        driver.find_element(By.XPATH, H.submit_form).click()

        driver.switch_to.frame(1)

        # Manually solve the CAPTCHA challenge
        time.sleep(15)

        # Check if the form submission was successful
        expected_message_text = "Thank you for your submission!"
        time.sleep(15)
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='kuTaGy wixui-button zKbzSQ']")))

        # Get the actual text of the element
        text = element.text

        try:
            assert text == expected_message_text, f"Text is '{text}', expected '{expected_message_text}'"
            print("Expected message text is displayed - Thank you for your submission!")
        except AssertionError:
            print("Submitting form was unsuccessful - Test is 'FAIL' cause user can't submit the form!")
            # Take a screenshot of the page
            driver.get_screenshot_as_file("Submitting form was unsuccessful.png")

    def test_chrome_event_Registration_form(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 1 - Verify Registration for event with invalid first and last name (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Scroll to "Upcoming Events " menu
        H.scroll_to_element(driver, H.event_menu)

        # Verify that "Event 2" is present
        wait.until(EC.visibility_of_element_located((By.XPATH, H.event_2)))
        # Verify that "RSVP" button for Event 2 is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, H.event_2)))

        # Click on button "Event 2"
        try:
            driver.find_element(By.XPATH, H.event_2).click()
            print("Button 'Event 2' is OK")
        except NoSuchElementException:
            print("Button 'Event 2' Doesn't work")
        time.sleep(3)

        # Verify that Title is correct !
        H.assert_title(driver, "Event 2 | California Marketing")
        time.sleep(2)

        # Verify text "Event 2" is present
        assert "Event 2" in driver.page_source

        #  Verify "Location" and print it
        print('Location is present: ', driver.find_element(By.XPATH, H.location).text)

        # Verify "Full DATE" and print it
        print('Time is present:  ',
              driver.find_element(By.XPATH, H.date).text)

        # Verify that Button "RSVP" is Visible and Clickable and Click on it !
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, H.rsvp_btn)))
            wait.until(EC.element_to_be_clickable((By.XPATH, H.rsvp_btn)))
            driver.find_element(By.XPATH, H.rsvp_btn).click()
            print("User get into RVSP")
        except TimeoutException:
            print("Button for Inner 'Event 2' Doesn't work")
        time.sleep(3)

        # List of special characters
        special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=']
        # Generate a random string of special characters
        random_special_chars = ''.join(
            random.choice(special_characters) for _ in range(10))  # Generate a string of 10 characters

        # Clear fields and type user's "invalid" first name
        driver.find_element(By.XPATH, H.first_name).clear()
        driver.find_element(By.XPATH, H.first_name).send_keys(random_special_chars)
        H.delay()

        # Clear fields and type user's "invalid" last name
        driver.find_element(By.XPATH, H.last_name).clear()
        driver.find_element(By.XPATH, H.last_name).send_keys(random_special_chars)
        H.delay()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.e_email).clear()
        driver.find_element(By.XPATH, H.e_email).send_keys(H.fakeEmail)
        H.delay()

        # Submit
        driver.find_element(By.XPATH, H.submit).click()
        H.delay()

        # Verify that Registration was Successful
        expected_message_text = "Thank you! See you soon"
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Thank you! See you soon']")))
        # Get the actual text of the element
        text = element.text

        try:
            assert text == expected_message_text, f"Text is '{text}', expected '{expected_message_text}'"
            print("Expected message text is displayed - Thank you! See you soon")
        except AssertionError:
            print("Submitting form was unsuccessful - Test is 'FAIL' cause user can register for the event with "
                  "invalid name and last name!")

    def test_chrome_Shopping_Cart_0_value(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 2 - Add 0 value to shopping cart   (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Locate and Click on Shop menu
        driver.find_element(By.XPATH, H.shop_button).click()
        H.delay()

        # Click on product 11 "Bow"
        driver.find_element(By.XPATH, H.product_11).click()
        H.delay()

        # Verify Quantity, by default is 1
        wait.until(EC.visibility_of_element_located((By.XPATH, H.quantity_def)))

        # Find the quantity field and clear its value
        driver.find_element(By.XPATH, H.quantity_field).clear()

        # Enter a value of 0 in the quantity field
        driver.find_element(By.XPATH, H.quantity_field).send_keys(0)

        # Verify that  "Add to Cart" button is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.cart_button)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.cart_button)))
        time.sleep(3)

        # Add product to cart
        driver.find_element(By.XPATH, H.cart_button).click()
        time.sleep(5)

        # Wait for the error message indicating a minimum quantity of 1
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Enter a minimum amount of 1')]")))

        # Assert that the error message is displayed
        try:
            assert "Enter a minimum amount of 1" in driver.page_source
            print("Minimum quantity validation passed!")
        except AssertionError:
            print("Minimum quantity validation failed!")

    def test_chrome_Sign_Up_invalid_email(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 3 - Sign-up on website with invalid email and valid password  (Chrome Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Verify that Main log in is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.main_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.main_login)))
        time.sleep(7)
        driver.find_element(By.XPATH, H.main_login).click()
        H.delay()

        # Verify that button "Sign Up With Email" is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.sign_up_with_email)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.sign_up_with_email)))
        driver.find_element(By.XPATH, H.sign_up_with_email).click()
        H.delay()

        # Fill in the sign-up form with invalid email
        email_field = driver.find_element(By.XPATH, H.e_signup)
        email_field.clear()
        email_field.send_keys("A@b@c@example.co")

        password_field = driver.find_element(By.XPATH, H.p_signup)
        password_field.clear()
        password_field.send_keys(1234)

        # Submit the sign-up form
        signup_button = driver.find_element(By.XPATH, H.signup_btn)
        signup_button.click()

        # Wait for the error message indicating the need to double-check the email
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[@id='siteMembersInputErrorMessage_emailInput_SM_ROOT_COMP747']")))

        # Assert that the error message is displayed
        try:
            assert "Double check your email and try again" in driver.page_source
            print("Test is 'PASS' - Sign-up with invalid email is not allowed!")
        except AssertionError:
            print("Test is 'FAIL' - Sign-up with invalid email was allowed!")

    def tearDown(self):
        self.driver.quit()


class Edge_California_Marketing(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        self.driver.maximize_window()

    def test_edge_verify_website_link(self):
        driver = self.driver
        # Open URL - home page
        driver.get(H.QASV_URL)
        driver.maximize_window()
        # Set another Window Size
        # driver.set_window_size(1200, 800)

        print("Positive_Test")
        print("TEST 1 - Verify Website Link  (Edge Browser) \n")

        # Check API Response Code
        print("California Marketing Url has", requests.get(H.QASV_URL).status_code, "as status Code")
        code = requests.get(H.QASV_URL).status_code
        if code == 200:
            print("API response code is OK")
        else:
            print("API response code is not 200", "Current code is:", code)

        # Check Title is correct
        try:
            assert "Home | California Marcketing" in driver.title
        except AssertionError:
            print("Driver title in Chrome is:", driver.title)

        # Check that the LOGO is present
        H.check_logo_presence(driver, (By.XPATH, H.Page_logo))

        # Check "California Marketing" page functionality
        wait = WebDriverWait(driver, 3)

        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Home_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Blog_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Shop_menu))
        H.check_menu_visibility_and_clickable(driver, (By.XPATH, H.Services_menu))

    def test_edge_Sign_Up(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 2 - Sign-up on website  (Edge Browser) \n")

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

    def test_edge_Sign_In(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 3 - Verify login with valid username and password  (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        time.sleep(4)

        # Verify that Main log in is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.main_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.main_login)))
        driver.find_element(By.XPATH, H.main_login).click()
        H.delay()

        # Switch from 'Sign Up' to 'Log In'
        wait.until(EC.visibility_of_element_located((By.XPATH, H.inner_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.inner_login)))
        driver.find_element(By.XPATH, H.inner_login).click()

        # Set wait until button 'Log In with Email' will be visible and click on it
        wait.until(EC.visibility_of_element_located((By.XPATH, H.login_with_email)))
        driver.find_element(By.XPATH, H.login_with_email).click()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.e_signin).clear()
        driver.find_element(By.XPATH, H.e_signin).send_keys(H.fakeEmail)
        driver.find_element(By.XPATH, H.e_signin).click()

        # Clear fields and type user's password
        driver.find_element(By.XPATH, H.p_signin).clear()
        driver.find_element(By.XPATH, H.p_signin).send_keys(H.fakePassword)
        driver.find_element(By.XPATH, H.p_signin).click()

        # Verify Final Log is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.last_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.last_login)))

        # Click on The button "Log In"
        driver.find_element(By.XPATH, H.last_login).click()
        time.sleep(10)

    def test_edge_Vk_link(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 4 - Validate Vk linked icon leads to correct page   (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Validate Vk linked icon leads to correct page:
        try:
            driver.find_element(By.XPATH, H.vk).click()
            print("Vk icon is clickable")
        except NoSuchElementException:
            print("Vk icon is NOT clickable")

        driver.switch_to.window(driver.window_handles[-1])

        # Verify correct Social media page was reached by URL:
        vkURL = driver.current_url
        if vkURL == H.vk_URL:
            print("Current Vk URL is correct:", driver.current_url)
        else:
            print("Vk URL is different from expected:", driver.current_url)

        # Verify correct Social media page was reached by Title:
        vk_expected_title = H.vk_Title
        if driver.title == vk_expected_title:
            print("Vk title is correct:", driver.title)
        else:
            print("Vk title is different from expected:", driver.title)

        # Verify correct Social media page was reached by Logo:
        try:
            driver.find_element(By.XPATH, H.vk_logo)
            print("Vk Logo was found")
        except NoSuchElementException:
            print("Vk Logo was not found")

        H.delay()

        # Verify Specific element is present on page:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located((By.XPATH, H.vk_follow)))
        try:
            driver.find_element(By.XPATH, H.vk_follow)
            print("Vk specific element is present on the opened page")
        except NoSuchElementException:
            print("No specific Vk element on the opened page")

        # Make driver back on previous page:
        driver.back()

        # Wait 1-3 sec:
        H.delay()

    def test_edge_Shopping_Cart(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 5 - Add to shopping cart a product and checkout   (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Locate and Click on Shop menu
        driver.find_element(By.XPATH, H.shop_button).click()

        # Click on product 6 "Blow-drier"
        driver.find_element(By.XPATH, H.product_6_button).click()

        # Verify Quantity, by default is 1
        wait.until(EC.visibility_of_element_located((By.XPATH, H.def_quantity)))

        # Verify that  "Add to Cart" button is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.cart_button)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.cart_button)))
        time.sleep(3)

        # Add product to cart
        driver.find_element(By.XPATH, H.cart_button).click()
        time.sleep(5)

        # Switch to "View Cart" frame
        driver.switch_to.frame(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, H.view_cart_btn)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.view_cart_btn)))
        driver.find_element(By.XPATH, H.view_cart_btn).click()
        # time.sleep(5)

        # Assert Driver Title
        H.assert_title(driver, 'Cart | California Marketing')
        time.sleep(5)

        # Function for Checkout
        H.checkout_product(driver)

        time.sleep(3)

        # Switch to "Checkout" frame
        driver.switch_to.frame(2)

        # Assert that User Cannot place an order
        H.verify_error_message(driver)

        print("Test is 'FAIL' cause user Can't place an order!")

    def test_edge_ConnectWithUs_form(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Positive_Test")
        print("TEST 6 - Verify Connect with us form  (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Scroll to "Connect with us" form
        H.scroll_to_element(driver, H.connect_w_us)

        # Assert that the text "CONECT WIT USS" is correct
        text_element = driver.find_element(By.XPATH, H.connect_w_us)
        text = text_element.text
        expected_text = "CONNECT WITH US"

        try:
            assert text == expected_text, f"Text is '{text}', expected '{expected_text}'"
        except AssertionError:
            # Print error message
            print("Assertion failed, text is different than expected")

        # Clear fields and type user's name
        driver.find_element(By.XPATH, H.name_field).clear()
        driver.find_element(By.XPATH, H.name_field).send_keys(H.fakeName)
        H.delay()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.email_field).clear()
        driver.find_element(By.XPATH, H.email_field).send_keys(H.fakeEmail)
        H.delay()

        # Clear fields and type user's subject
        driver.find_element(By.XPATH, H.subject_field).clear()
        driver.find_element(By.XPATH, H.subject_field).send_keys("Job")
        H.delay()

        # Clear fields and type user's message
        driver.find_element(By.XPATH, H.message_field).clear()
        driver.find_element(By.XPATH, H.message_field).send_keys("Hello!")
        H.delay()

        # Submit form
        wait.until(EC.element_to_be_clickable((By.XPATH, H.submit_form)))
        driver.find_element(By.XPATH, H.submit_form).click()

        driver.switch_to.frame(1)

        # Manually solve the CAPTCHA challenge
        time.sleep(15)

        # Check if the form submission was successful
        expected_message_text = "Thank you for your submission!"
        time.sleep(15)
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='kuTaGy wixui-button zKbzSQ']")))

        # Get the actual text of the element
        text = element.text

        try:
            assert text == expected_message_text, f"Text is '{text}', expected '{expected_message_text}'"
            print("Expected message text is displayed - Thank you for your submission!")
        except AssertionError:
            print("Submitting form was unsuccessful - Test is 'FAIL' cause user can't submit the form!")
            # Take a screenshot of the page
            driver.get_screenshot_as_file("Submitting form was unsuccessful.png")

    def test_edge_event_Registration_form(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 1 - Verify Registration for event with invalid first and last name (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Scroll to "Upcoming Events " menu
        H.scroll_to_element(driver, H.event_menu)

        # Verify that "Event 2" is present
        wait.until(EC.visibility_of_element_located((By.XPATH, H.event_2)))
        # Verify that "RSVP" button for Event 2 is clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, H.event_2)))

        # Click on button "Event 2"
        try:
            driver.find_element(By.XPATH, H.event_2).click()
            print("Button 'Event 2' is OK")
        except NoSuchElementException:
            print("Button 'Event 2' Doesn't work")
        time.sleep(3)

        # Verify that Title is correct !
        H.assert_title(driver, "Event 2 | California Marketing")
        time.sleep(2)

        # Verify text "Event 2" is present
        assert "Event 2" in driver.page_source

        #  Verify "Location" and print it
        print('Location is present: ', driver.find_element(By.XPATH, H.location).text)

        # Verify "Full DATE" and print it
        print('Time is present:  ',
              driver.find_element(By.XPATH, H.date).text)

        # Verify that Button "RSVP" is Visible and Clickable and Click on it !
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, H.rsvp_btn)))
            wait.until(EC.element_to_be_clickable((By.XPATH, H.rsvp_btn)))
            driver.find_element(By.XPATH, H.rsvp_btn).click()
            print("User get into RVSP")
        except TimeoutException:
            print("Button for Inner 'Event 2' Doesn't work")
        time.sleep(3)

        # List of special characters
        special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=']
        # Generate a random string of special characters
        random_special_chars = ''.join(
            random.choice(special_characters) for _ in range(10))  # Generate a string of 10 characters

        # Clear fields and type user's "invalid" first name
        driver.find_element(By.XPATH, H.first_name).clear()
        driver.find_element(By.XPATH, H.first_name).send_keys(random_special_chars)
        H.delay()

        # Clear fields and type user's "invalid" last name
        driver.find_element(By.XPATH, H.last_name).clear()
        driver.find_element(By.XPATH, H.last_name).send_keys(random_special_chars)
        H.delay()

        # Clear fields and type user's email
        driver.find_element(By.XPATH, H.e_email).clear()
        driver.find_element(By.XPATH, H.e_email).send_keys(H.fakeEmail)
        H.delay()

        # Submit
        driver.find_element(By.XPATH, H.submit).click()
        H.delay()

        # Verify that Registration was Successful
        expected_message_text = "Thank you! See you soon"
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Thank you! See you soon']")))
        # Get the actual text of the element
        text = element.text

        try:
            assert text == expected_message_text, f"Text is '{text}', expected '{expected_message_text}'"
            print("Expected message text is displayed - Thank you! See you soon")
        except AssertionError:
            print("Submitting form was unsuccessful - Test is 'FAIL' cause user can register for the event with "
                  "invalid name and last name!")

    def test_edge_Shopping_Cart_0_value(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 2 - Add 0 value to shopping cart   (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Locate and Click on Shop menu
        driver.find_element(By.XPATH, H.shop_button).click()
        H.delay()

        # Click on product 11 "Bow"
        driver.find_element(By.XPATH, H.product_11).click()
        H.delay()

        # Verify Quantity, by default is 1
        wait.until(EC.visibility_of_element_located((By.XPATH, H.quantity_def)))

        # Find the quantity field and clear its value
        driver.find_element(By.XPATH, H.quantity_field).clear()

        # Enter a value of 0 in the quantity field
        driver.find_element(By.XPATH, H.quantity_field).send_keys(0)

        # Verify that  "Add to Cart" button is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.cart_button)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.cart_button)))
        time.sleep(3)

        # Add product to cart
        driver.find_element(By.XPATH, H.cart_button).click()
        time.sleep(5)

        # Wait for the error message indicating a minimum quantity of 1
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Enter a minimum amount of 1')]")))

        # Assert that the error message is displayed
        try:
            assert "Enter a minimum amount of 1" in driver.page_source
            print("Minimum quantity validation passed!")
        except AssertionError:
            print("Minimum quantity validation failed!")

    def test_edge_Sign_Up_invalid_email(self):
        driver = self.driver
        driver.get(H.QASV_URL)
        driver.maximize_window()

        print("Negative_Test")
        print("TEST 3 - Sign-up on website with invalid email and valid password  (Edge Browser) \n")

        wait = WebDriverWait(driver, 3)

        # Check Title is correct
        H.assert_title(driver, "Home | California Marcketing")

        # Check API Response Code
        H.check_API_code(driver)

        # Verify that Main log in is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.main_login)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.main_login)))
        time.sleep(7)
        driver.find_element(By.XPATH, H.main_login).click()
        H.delay()

        # Verify that button "Sign Up With Email" is visible and clickable
        wait.until(EC.visibility_of_element_located((By.XPATH, H.sign_up_with_email)))
        wait.until(EC.element_to_be_clickable((By.XPATH, H.sign_up_with_email)))
        driver.find_element(By.XPATH, H.sign_up_with_email).click()
        H.delay()

        # Fill in the sign-up form with invalid email
        email_field = driver.find_element(By.XPATH, H.e_signup)
        email_field.clear()
        email_field.send_keys("A@b@c@example.co")

        password_field = driver.find_element(By.XPATH, H.p_signup)
        password_field.clear()
        password_field.send_keys(1234)

        # Submit the sign-up form
        signup_button = driver.find_element(By.XPATH, H.signup_btn)
        signup_button.click()

        # Wait for the error message indicating the need to double-check the email
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[@id='siteMembersInputErrorMessage_emailInput_SM_ROOT_COMP747']")))

        # Assert that the error message is displayed
        try:
            assert "Double check your email and try again" in driver.page_source
            print("Test is 'PASS' - Sign-up with invalid email is not allowed!")
        except AssertionError:
            print("Test is 'FAIL' - Sign-up with invalid email was allowed!")


    def tearDown(self):
        self.driver.quit()
