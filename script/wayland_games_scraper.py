import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WaylandGamesScraper:
    def __init__(self, driver):
        ''' 
            WaylandGamesScraper: 
            Class for extracting product data from Wayland Games. 
            Main methods include initialization and scraping product details. 
            Initialize the scraper with a Selenium WebDriver instance.
        '''
        self.driver = driver

    def scrape(self):
        '''Main method to scrape product data from Wayland Games.'''
        url = 'https://www.waylandgames.co.uk/'
        self.driver.get(url)
        time.sleep(5)  # time for the page to load

        product_data = []
        try:
            # Get menu links to different product categories
            menu_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.Row_pbRoot__8BKf_ a.button')
            menu_links = [button.get_attribute('href') for button in menu_buttons]
        except Exception as e:
            logger.error("Error retrieving menu links: %s", str(e))
            return []

        for link in menu_links:
            self.driver.get(link)
            time.sleep(5)  # time for the page to load

            while True: 
                try:
                    # Retrieve product details
                    products = self.driver.find_elements(By.CLASS_NAME, 'ProductCard_productDetails__4HJNp')
                except Exception as e:
                    logger.error("Error retrieving products from %s: %s", link, str(e))
                    break

                for product in products:
                    try:
                        title = product.find_element(By.CLASS_NAME, 'ProductCard_productName__zdXR5').text
                        stock_status = product.find_element(By.CLASS_NAME, 'StockStatus_statusStockInStock__zEcJQ').text
                        price = product.find_element(By.CLASS_NAME, 'Price_priceNow__OV_3o').text
                        product_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    except Exception as e:
                        logger.warning("Error retrieving product details: %s", str(e))
                        title, stock_status, price, product_url = 'N/A', 'N/A', 'N/A', 'N/A'

                    product_info = {
                        'Product Title': title,
                        'Product URL': product_url,
                        'Price': price,
                        'Stock Level': stock_status,
                    }

                    product_data.append(product_info)

                try:
                    # Navigate to the next page if available
                    next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Next"]')))
                    if "Pagination_paginationLinkDisabled__tOy09" in next_button.get_attribute("class"):
                        break
                    next_button.click()
                    time.sleep(5)
                except Exception as e:
                    logger.info("No more pages to scrape from this section: %s", str(e))
                    break

        return product_data
