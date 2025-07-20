import os
import time
import logging
import argparse
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure logging for professional output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flight_search.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoibiboFlightSearch:
    """
    Automates flight search on Goibibo using Selenium WebDriver.
    """
    def __init__(self, headless=False, login_mode=False, user_data_dir=None):
        self.headless = headless
        self.login_mode = login_mode
        self.user_data_dir = user_data_dir
        self.driver = self._init_driver()
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if self.headless:
            options.add_argument("--headless=new")
        if self.login_mode and self.user_data_dir:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
            logger.info(f"Using Chrome profile from: {self.user_data_dir}")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def take_screenshot(self, name):
        """Take a screenshot with a timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename

    def handle_popups(self):
        """Handle and close login popups if present."""
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.logSprite.icClose"))
            )
            close_btn.click()
            logger.info("Closed login popup")
            time.sleep(1)
        except TimeoutException:
            logger.info("No login popup found")

    def enter_city(self, selector, city_name, airport_code):
        """Enter a city and select the airport code from the dropdown. Updated for Goibibo July 2025 UI."""
        try:
            # Click the input field (label or input)
            input_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            input_field.click()
            time.sleep(1)
            # Find the actual input box (it may be the next input[type='text'] or visible input)
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and not(@readonly)]"))
            )
            input_box.clear()
            input_box.send_keys(city_name)
            time.sleep(2)
            # Wait for dropdown and select by airport code
            airport_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{airport_code}') or contains(., '{city_name}')][1]"))
            )
            airport_option.click()
            logger.info(f"Selected city: {city_name} ({airport_code})")
            return True
        except Exception as e:
            logger.error(f"Error entering city: {e}")
            self.take_screenshot(f"error_city_{airport_code}")
            return False

    def select_date(self, days_from_today=5):
        """Select a departure date days_from_today from now."""
        try:
            target_date = datetime.now() + timedelta(days=days_from_today)
            date_str = target_date.strftime("%a %b %d %Y")

            date_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Departure']"))
            )
            date_field.click()
            time.sleep(1)

            date_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{date_str}']"))
            )
            date_element.click()
            logger.info(f"Selected departure date: {date_str}")
            return True
        except Exception as e:
            logger.error(f"Error selecting date: {e}")
            self.take_screenshot("error_selecting_date")
            return False

    def perform_search(self):
        """Click the search button to perform the flight search."""
        try:
            search_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Search Flights']/ancestor::button"))
            )
            search_btn.click()
            logger.info("Clicked search button")
            return True
        except Exception as e:
            logger.error(f"Error clicking search: {e}")
            self.take_screenshot("error_clicking_search")
            return False

    def verify_search_results(self):
        """Verify that flight results are present on the results page."""
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.fltResultWrapper"))
            )
            flights = self.driver.find_elements(By.CSS_SELECTOR, "div.fltResultWrapper")
            if flights:
                logger.info(f"Found {len(flights)} flight results.")
                return True
            else:
                logger.warning("No flights found.")
                return False
        except TimeoutException:
            logger.error("Timeout waiting for search results.")
            self.take_screenshot("timeout_results")
            return False
        except Exception as e:
            logger.error(f"Error verifying results: {e}")
            self.take_screenshot("error_verifying_results")
            return False

    def run_search(self, from_city, from_code, to_city, to_code, departure_days=5):
        """
        Run the full flight search process.
        Returns True if successful, False otherwise.
        """
        try:
            self.driver.get("https://www.goibibo.com/flights/")
            logger.info("Opened Goibibo flight page.")
            self.take_screenshot("01_homepage")

            self.handle_popups()

            if not self.enter_city("input[placeholder='From']", from_city, from_code):
                return False
            if not self.enter_city("input[placeholder='To']", to_city, to_code):
                return False
            if not self.select_date(departure_days):
                return False

            self.take_screenshot("02_before_search")

            if not self.perform_search():
                return False

            self.take_screenshot("03_after_search")

            result = self.verify_search_results()
            self.take_screenshot("04_results")
            return result
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.take_screenshot("unexpected_error")
            return False
        finally:
            self.driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Goibibo Flight Search Automation')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--login', action='store_true', help='Use logged-in session')
    parser.add_argument('--user-data-dir', type=str, help='Chrome user data directory for logged-in session')
    args = parser.parse_args()

    logger.info("Starting Goibibo Flight Search Script")
    logger.info(f"Mode: {'Login' if args.login else 'Guest'}, Headless: {args.headless}")

    searcher = GoibiboFlightSearch(
        headless=args.headless,
        login_mode=args.login,
        user_data_dir=args.user_data_dir
    )

    # Customize source/destination as needed
    success = searcher.run_search(
        from_city="Delhi",
        from_code="DEL",
        to_city="Mumbai",
        to_code="BOM",
        departure_days=5
    )

    if success:
        logger.info("Flight search completed successfully!")
    else:
        logger.error("Flight search failed.")