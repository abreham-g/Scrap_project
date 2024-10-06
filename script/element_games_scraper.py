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

class ElementGamesScraper:
    def __init__(self, driver):
        ''' 
        ElementGamesScraper: 
        Class for extracting product data from Element Games. 
        Main methods include initialization and scraping product details. 
        Initialize the scraper with a Selenium WebDriver instance
        '''
        self.driver = driver

    def scrape(self):
        '''Main method to scrape product data from Element Games.'''
        urls = ['https://elementgames.co.uk/board-games',
                'https://elementgames.co.uk/games-workshop',
                'https://elementgames.co.uk/paints-hobby-and-scenery']  
        product_data = []

        for url in urls:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'productinfo')))

            while True:
                try:
                    # Retrieve product details
                    products = self.driver.find_elements(By.CLASS_NAME, 'productinfo')
                except Exception as e:
                    logger.error("Error retrieving products from %s: %s", url, str(e))
                    break

                for product in products:
                    title = product.find_element(By.CLASS_NAME, 'producttitle').text if product.find_elements(By.CLASS_NAME, 'producttitle') else 'N/A'
                    price = product.find_element(By.CLASS_NAME, 'price').text if product.find_elements(By.CLASS_NAME, 'price') else 'N/A'
                    
                    try:
                        # Determine stock status
                        stock_info = product.find_element(By.CLASS_NAME, 'stock_popup').text                
                        stock_status = 'N/A'
                        
                        if "In Stock" in stock_info:
                            stock_level = stock_info.split(' ')[0]
                            stock_status = f"{stock_level} In Stock"
                        elif "Stock Due" in stock_info:
                            stock_status = 'Stock Due'
                        elif "Backorder" in stock_info:
                            stock_status = 'Available for Backorder'
                    except Exception:
                        stock_status = 'N/A'

                    product_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href') if product.find_elements(By.TAG_NAME, 'a') else 'N/A'

                    product_info = {
                        'Product Title': title,
                        'Product URL': product_url,
                        'Price': price,
                        'Stock Level': stock_status,
                    }

                    product_data.append(product_info)

                try:
                    # Navigate to next page if available
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Next"]'))
                    )
                    next_button.click()
                    time.sleep(5) 
                except Exception as e:
                    logger.info("No more pages to scrape for URL: %s. %s", url, str(e))
                    break

        return product_data

