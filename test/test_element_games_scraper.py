import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from script.element_games_scraper import ElementGamesScraper

class TestElementGamesScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''Set up the WebDriver for testing.'''
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        cls.service = Service('/usr/local/bin/chromedriver')
        cls.driver = webdriver.Chrome(service=cls.service, options=chrome_options)

    @classmethod
    def tearDownClass(cls):

        '''Quit the WebDriver after tests.'''
        
        cls.driver.quit()

    def test_scraper_initialization(self):

        '''Test that the scraper can be initialized.'''

        scraper = ElementGamesScraper(self.driver)
        self.assertIsInstance(scraper, ElementGamesScraper)

    def test_scrape(self):

        '''Test that the scrape method returns data.'''

        scraper = ElementGamesScraper(self.driver)
        data = scraper.scrape()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)  # Ensure some data is returned
        self.assertIn('Product Title', data[0])
        self.assertIn('Product URL', data[0])
        self.assertIn('Price', data[0])
        self.assertIn('Stock Level', data[0])

if __name__ == '__main__':
    unittest.main()