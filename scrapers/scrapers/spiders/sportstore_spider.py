import time

from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class SportStoreSpider(CrawlSpider):
    name = 'sportstore_crawl'
    allowed_domain = ['thesportstore.pk']
    start_urls = ['https://www.thesportstore.pk/']

    def parse_start_url(self, response, BY=None, **kwargs):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.start_urls[0])
        amount_of_categories = len(driver.find_elements(By.CSS_SELECTOR, ".xs-25"))
        for index in range(1, amount_of_categories + 1):
            selector = f".xs-25:nth-child({index})"
            element = driver.find_element(By.CSS_SELECTOR, selector)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element)).click()
            category_page_url = driver.current_url

            if len(driver.find_elements(By.CSS_SELECTOR, ".main-posts")) == 0 and len(
                    driver.find_elements(By.CSS_SELECTOR, ".product-grid-item")) > 0:
                pagination = len(driver.find_elements(By.CSS_SELECTOR, ".pagination > div > ul > li")) - 2
                for page in range(1, pagination + 1):
                    driver.get(category_page_url + f"#/sort=p.sort_order/order=ASC/limit=16/page={page}")
                    page_url = driver.current_url

                    products_on_page = len(driver.find_elements(By.CSS_SELECTOR, ".product-grid-item"))
                    for index2 in range(1, products_on_page + 1):
                        time.sleep(2)
                        try:
                            selector_2 = f".product-grid-item:nth-child({index2})>div>.image"
                            element2 = driver.find_element(By.CSS_SELECTOR, selector_2)
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element2)).click()
                            item = {
                                "title": driver.find_element(By.CSS_SELECTOR, ".heading-title").text,
                                'brand': driver.find_element(By.CSS_SELECTOR, ".p-brand a").text,
                                'product-code': driver.find_element(By.CSS_SELECTOR, ".p-model span").text,
                                'price': driver.find_element(By.CSS_SELECTOR, ".product-price").text,
                                'options': [x.text for x in driver.find_elements(By.CSS_SELECTOR,
                                                                                 ".list-unstyled.price + .options option:nth-child(n+2)")],
                                'main-image': driver.find_element(By.CSS_SELECTOR, "div.image a").get_attribute('href'),
                                'description': driver.find_element(By.CSS_SELECTOR, "div#tab-description").text,
                                'images': [x.get_attribute('href') for x in
                                           driver.find_elements(By.CSS_SELECTOR, "#product-gallery a")]
                            }
                            yield item
                        except NoSuchElementException:
                            print(driver.current_url)

                        ##here

                        driver.get(page_url)
                driver.get(category_page_url)

            amount_of_subcategories = len(driver.find_elements(By.CSS_SELECTOR, ".main-posts"))
            for index1 in range(1, amount_of_subcategories + 1):
                selector_1 = f".main-posts:nth-child({index1}) > div"
                element1 = driver.find_element(By.CSS_SELECTOR, selector_1)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element1)).click()
                subcategory_url = driver.current_url

                pagination = len(driver.find_elements(By.CSS_SELECTOR, ".pagination > div > ul > li")) - 2
                for page in range(1, pagination + 1):
                    driver.get(subcategory_url + f"#/sort=p.sort_order/order=ASC/limit=16/page={page}")
                    page_url = driver.current_url

                    products_on_page = len(driver.find_elements(By.CSS_SELECTOR, ".product-grid-item"))
                    for index2 in range(1, products_on_page + 1):
                        time.sleep(2)
                        try:
                            selector_2 = f".product-grid-item:nth-child({index2})>div>.image"
                            element2 = driver.find_element(By.CSS_SELECTOR, selector_2)
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element2)).click()
                            item = {
                                "title": driver.find_element(By.CSS_SELECTOR, ".heading-title").text,
                                'brand': driver.find_element(By.CSS_SELECTOR, ".p-brand a").text,
                                'product-code': driver.find_element(By.CSS_SELECTOR, ".p-model span").text,
                                'price': driver.find_element(By.CSS_SELECTOR, ".product-price").text,
                                'options': [x.text for x in driver.find_elements(By.CSS_SELECTOR, ".list-unstyled.price + .options option:nth-child(n+2)")],
                                'main-image': driver.find_element(By.CSS_SELECTOR, "div.image a").get_attribute('href'),
                                'description': driver.find_element(By.CSS_SELECTOR, "div#tab-description").text,
                                'images': [x.get_attribute('href') for x in driver.find_elements(By.CSS_SELECTOR, "#product-gallery a")]
                                }
                            yield item
                        except NoSuchElementException:
                            pass

                        driver.get(page_url)

                driver.get(category_page_url)
            driver.get(self.start_urls[0])
