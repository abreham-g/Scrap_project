import os
import sys
import logging
import pandas as pd
sys.path.append(os.path.abspath(os.path.join('./script')))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from wayland_games_scraper import WaylandGamesScraper
from element_games_scraper import ElementGamesScraper



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GameScraper:
    ''' 
        GameScraper: 
        Main class to manage the scraping process for both Wayland and Element Games. 
        Includes methods for saving data and executing the scraping process. 
    '''
    def __init__(self):
        '''Initialize the WebDriver and output directory.'''
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize WebDriver service
        self.service = Service('/usr/local/bin/chromedriver')  
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.output_dir = '../Data'
        os.makedirs(self.output_dir, exist_ok=True)
        

    def save_data(self, wayland_data, element_data):
        '''Save scraped data to CSV files.'''
        wayland_df = pd.DataFrame(wayland_data)
        wayland_df['Product Title'] = wayland_df['Product Title'].str.split('\n').str[0]
        wayland = wayland_df.dropna(subset=['Product Title'])
        wayland.to_csv(os.path.join(self.output_dir, 'wayland_games_data.csv'), index=False)
        logger.info("Wayland Games data saved to %s", os.path.join(self.output_dir, 'wayland_games_data.csv'))
        element_df = pd.DataFrame(element_data)
        element_df['Stock Level'] = '10+ in stock'
        element=element_df
        element.to_csv(os.path.join(self.output_dir, 'element_games_data.csv'), index=False)
        logger.info("Element Games data saved to %s", os.path.join(self.output_dir, 'element_games_data.csv'))
        logger.info("wayland data:\n%s", wayland_df)
        logger.info("Element data:\n%s", element_df)

    def run(self):
        '''Run the scraping process for both Wayland and Element Games.'''
        wayland_scraper = WaylandGamesScraper(self.driver)
        element_scraper = ElementGamesScraper(self.driver)
        wayland_data = wayland_scraper.scrape()
        element_data = element_scraper.scrape()
        self.save_data(wayland_data, element_data)

        # Quit the driver
        self.driver.quit()

if __name__ == "__main__":
    scraper = GameScraper()
    scraper.run()

