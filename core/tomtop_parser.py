import sys
from os.path import basename
from urllib.parse import urlparse

import requests
from requests.exceptions import MissingSchema, ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.xpath_variables import ThingsXpath as Xpath

key_result_title = "title"
key_result_subtitle = "subtitle"
key_result_description = "description"
key_result_regular_price = "regular_price"
key_result_sale_price = "sale_price"
key_result_product_options = "product_options"
key_result_product_rating = "product_rating"
key_result_product_shipping = "product_shipping"
key_result_regular_image = "image"


class TomtopShopParser:

    def __init__(self, product_link):
        self._url = product_link

    def get_content(self):
        """ Parse all important data"""
        result_structure = {}
        try:
            self._create_web_driver()
            result_structure[key_result_title] = self._get_title()
            result_structure[key_result_subtitle] = self._get_subtitle()
            result_structure[key_result_description] = self._get_description()
            result_structure[key_result_regular_price] = self._get_regular_price()
            result_structure[key_result_sale_price] = self._get_sale_value()
            result_structure[key_result_product_options] = self._get_available_options()
            result_structure[key_result_product_rating] = self._get_product_rating()
            result_structure[key_result_product_shipping] = self._shipping_info()
            result_structure[key_result_regular_image] = self._get_things_photo()
            return result_structure

        except MissingSchema as e:
            print(f"The link {self._url} is broken: {e}")
        except ConnectionError as _:
            print(f"Internet connection error. Your link is bullshit.")
            sys.exit(1)
        except Exception as e:
            print(f"There is exception in the process of parsing: {e}")
        return {}

    def _create_web_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.headless = True
        self._driver = webdriver.Chrome(options=chrome_options)
        self._driver.get(url=self._url)
        self._click_event(Xpath.site_cookies_button)
        self._click_event(Xpath.country_button_main)
        self._click_event(Xpath.language_options)
        self._click_event(Xpath.language_option_en)
        self._click_event(Xpath.country_options)
        self._click_event(Xpath.country_options_en)
        self._click_event(Xpath.currency)
        self._click_event(Xpath.currency_option_en)
        self._click_event(Xpath.button_save)

    def _get_title(self):
        """ Parse title of a product """
        try:
            return self._driver.find_element(By.XPATH, Xpath.product_title).text
        except Exception as e:
            print(f"Exception while parsing the title : {e}")
            return ""

    def _get_subtitle(self):
        """ Parse subtitle of a product """
        try:
            return self._driver.find_element(By.XPATH, Xpath.product_subtitle).text
        except Exception as e:
            print(f"Exception while parsing the subtitle : {e}")
            return ""

    def _get_description(self):
        """Parse description of product"""
        try:
            return self._driver.find_element(By.XPATH, Xpath.product_description).text
        except Exception as e:
            print(f"Exception while parsing the description : {e}")
            return ""

    def _get_regular_price(self):
        """Parse regular price of product"""
        try:
            regular_price_usd = self._driver.find_element(By.XPATH, Xpath.product_regular_price).get_attribute(
                "usvalue")
            return f"Original Price: {regular_price_usd} US"
        except Exception as e:
            print(f"Exception while parsing the regular price : {e}")
            return f"Can`t retrieve regular price correctly. See sale price as Regular."

    def _get_sale_value(self):
        """Parse sale price of product"""
        try:
            sale_price_usd = self._driver.find_element(By.XPATH, Xpath.product_sale_price_usd).get_attribute("usvalue")
            return f"Sale Price: {sale_price_usd} US"
        except Exception as e:
            print(f"Exception while parsing the sale price : {e}")
            return f"Can`t retrieve sale price correctly. Website`s code is bad to read."

    def _get_product_rating(self):
        try:
            rating = self._driver.find_element(By.XPATH, Xpath.product_rating_value).get_attribute("textContent")
            reviews = self._driver.find_element(By.XPATH, Xpath.product_review_count).text
            return f"Product rating: {rating}; review count: {reviews}"
        except Exception as e:
            print(f"Exception while parse the thing rating: {e}")
            return f"Can`t retrieve rating of current thing."

    def _get_available_options(self):
        try:
            options_container = self._driver.find_element(By.XPATH, Xpath.product_options_container)
            if options_container is None:
                return "Options: No options on this product."

            options_type_title = options_container.find_element(By.XPATH, Xpath.product_option_name)
            options_list = self._driver.find_elements(By.XPATH, Xpath.product_available_options)
            if options_list is not None:
                result_output = f"Available {options_type_title.text} "
                for item in options_list:
                    result_output += item.get_attribute("data-attr-value") + "; "
            else:
                return "Can`t retrieve available options or they are not available."

            return result_output

        except Exception as e:
            print(f"Error while retrieve options of thing: {e}")
            return "Can`t retrieve available options or they are not available."

    def _get_things_photo(self):
        image_src = self._driver.find_element(By.XPATH, Xpath.product_title_image).get_attribute("href")
        img_data = requests.get(image_src).content
        img_name = basename(urlparse(image_src).path)
        with open("images/" + img_name, 'wb') as handler:
            handler.write(img_data)

        return image_src

    def _shipping_info(self):
        result_delivery = ""
        try:
            warehouses = self._driver.find_elements(By.XPATH, Xpath.product_warehouses)
            for warehouse in warehouses:
                if not warehouse.is_selected():
                    warehouse.click()

                self._click_event(Xpath.product_delivery_logistics)
                shipping_methods = self._driver.find_elements(By.XPATH, Xpath.product_shipping_methods)
                result_delivery += "<!-- wp:paragraph --><p>" + warehouse.get_attribute(
                    "title") + ":</p><!-- /wp:paragraph -->"
                if len(shipping_methods) == 0:
                    result_delivery += "No delivery from this warehouse.\n\n"
                else:
                    for single_shipping_method in shipping_methods:
                        name_of_option = single_shipping_method.find_element(By.XPATH,
                                                                             Xpath.product_delivery_option_name) \
                            .get_attribute("textContent")
                        estimated_shipping_time = single_shipping_method.find_element(By.XPATH,
                                                                                      Xpath.product_delivery_time) \
                            .get_attribute("textContent")
                        tracking_number = single_shipping_method.find_element(By.XPATH,
                                                                              Xpath.product_delivery_tracking_number) \
                            .get_attribute("textContent")
                        shipping_cost = single_shipping_method.find_element(By.XPATH,
                                                                            Xpath.product_delivery_shipping_cost) \
                            .get_attribute("textContent")
                        result_delivery += f"<!-- wp:paragraph --><p>Name:{name_of_option} Time shipping:{estimated_shipping_time} " \
                                           f"Tracking:{tracking_number} Delivery cost:{shipping_cost}</p><!-- /wp:paragraph -->"
                self._click_event(Xpath.exit_shipping_dialog)
        except Exception as e:
            print(f"Error while parse delivery options: {e}")

        return result_delivery

    def _click_event(self, xpath):
        WebDriverWait(driver=self._driver, timeout=20).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def set_url(self, new_url):
        self._url = new_url

    def get_url(self):
        return self._url
