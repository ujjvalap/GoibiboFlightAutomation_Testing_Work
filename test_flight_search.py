import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from flight_search import GoibiboFlightSearch

class TestGoibiboFlightSearch(unittest.TestCase):
    @patch('flight_search.webdriver.Chrome')
    def setUp(self, mock_chrome):
        # Mock Chrome driver and its methods
        self.mock_driver = MagicMock()
        mock_chrome.return_value = self.mock_driver
        self.searcher = GoibiboFlightSearch(headless=True)

    def test_enter_city_success(self):
        # Setup mocks for city entry
        self.mock_driver.find_elements.return_value = [MagicMock()]
        with patch('flight_search.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            result = self.searcher.enter_city('input[placeholder="From"]', 'Delhi', 'DEL')
            self.assertTrue(result)

    def test_select_date_success(self):
        with patch('flight_search.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            result = self.searcher.select_date(5)
            self.assertTrue(result)

    def test_perform_search_success(self):
        with patch('flight_search.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            result = self.searcher.perform_search()
            self.assertTrue(result)

    def test_verify_search_results_found(self):
        self.mock_driver.find_elements.return_value = [MagicMock(), MagicMock()]
        with patch('flight_search.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            result = self.searcher.verify_search_results()
            self.assertTrue(result)

    def test_verify_search_results_not_found(self):
        self.mock_driver.find_elements.return_value = []
        with patch('flight_search.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            result = self.searcher.verify_search_results()
            self.assertFalse(result)

    def tearDown(self):
        self.searcher.driver.quit()

if __name__ == '__main__':
    unittest.main()