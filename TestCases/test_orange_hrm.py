import os
import pytest
import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PageObjects.login_page import Login
from PageObjects.dashboard_page import Dashboard
from PageObjects.leave_page import Leave


@pytest.mark.usefixtures("setup")
class TestOrangeHRM:
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.screenshots_dir = os.path.join(base_dir, "Screenshots", f"test_run_{self.run_timestamp}")
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def save_screenshot(self, test_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not hasattr(self, 'screenshots_dir'):
            self.setUp()

        path = os.path.join(self.screenshots_dir, f"{test_name}_{timestamp}.png")
        self.driver.save_screenshot(path)


    def test_01_login_page_title(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        time.sleep(1)
        actual_title = self.driver.title
        expected_title = "OrangeHRM"

        if actual_title == expected_title:
            self.save_screenshot("test_01_login_page_title")
            assert True
        else:
            self.save_screenshot("test_01_login_page_title_failed")
            assert False, f"Expected title: {expected_title}, but got: {actual_title}"

    def test_02_login(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        time.sleep(1)

        login_page = Login(self.driver)
        dashboard_page = Dashboard(self.driver)
        login_page.login("Admin", "admin123")

        if dashboard_page.verify_dashboard_page():
            self.save_screenshot("test_02_login")
            assert True
        else:
            self.save_screenshot("test_02_login_failed")
            assert False, "Dashboard not loaded after login"

    def test_03_leave_functionality(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        login_page = Login(self.driver)
        dashboard_page = Dashboard(self.driver)
        leave_page = Leave(self.driver)

        try:
            if login_page.is_on_login_page():
                login_page.login("Admin", "admin123")

            if not dashboard_page.verify_dashboard_page():
                self.save_screenshot("test_03_dashboard_not_loaded")
                assert False, "Dashboard not loaded"

            leave_sidebar_item = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Leave']"))
            )
            leave_sidebar_item.click()

            my_leave_tab = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='My Leave']"))
            )
            my_leave_tab.click()

            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//h5[text()='My Leave List']"))
            )

            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'oxd-table')]"))
            )

            self.save_screenshot("test_03_leave_functionality")

            if leave_page.verify_leave_page():
                assert True
            else:
                self.save_screenshot("test_03_leave_page_verification_failed")
                assert False, "Leave page not verified"

        except TimeoutException as e:
            self.save_screenshot("test_03_leave_functionality_timeout")
            assert False, f"Timeout occurred: {str(e)}"

        except Exception as e:
            self.save_screenshot("test_03_leave_functionality_error")
            assert False, f"Unexpected error occurred: {str(e)}"

    def test_04_logout(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        login_page = Login(self.driver)
        dashboard_page = Dashboard(self.driver)

        try:
            if login_page.is_on_login_page():
                login_page.login("Admin", "admin123")

            if not dashboard_page.verify_dashboard_page():
                self.save_screenshot("test_04_dashboard_not_loaded")
                assert False, "Dashboard not loaded"

            time.sleep(1)
            dashboard_page.click_logout()

            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.NAME, login_page.txt_username_name))
            )

            assert self.driver.find_element(By.NAME, login_page.txt_username_name).is_displayed(), \
                "Login field not displayed after logout"

            self.save_screenshot("test_04_logout")

        except Exception as e:
            self.save_screenshot("test_04_logout_error")
            assert False, f"Logout test failed: {str(e)}"