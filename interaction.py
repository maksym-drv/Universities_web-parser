from data import *
from time import sleep
import json
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

specialities = ['122', '123']

class Interaction:
    __list_button_path      = '//*[@id="search-form-general"]/div[2]/div/div[1]/button'
    __spec_input_path       = '/html/body/div[2]/div/div[1]/input'
    __select_spec_path      = '//*[@id="bs-select-3"]/ul'
    __search_button_id      = 'offers-search-button'
    __university_id         = 'universities'
    __university_cl         = 'university'

    __university_offers     = 'university-offers'
    __university_offers     = 'university-offers'
    __university_offers_qbe = 'university-offers-qbe'
    __university_title      = 'university-offers-title'

    __offer                 = 'offer'
    __offer_info            = 'offer-info'
    __offer_info_left       = 'offer-info-left'
    __offer_name            = 'row offer-university-specialities-name'
    
    def __init__(self, url: str = 'https://vstup.edbo.gov.ua/offers/') -> None:
        options = webdriver.FirefoxOptions()
        options.binary_location = r'/usr/bin/firefox'
        options.add_argument("--headless")
        self.__driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.__url = url
        sleep(1)

    def __interact(func) -> str:

        def wrapper(self, speciality: str):

            self.__driver.get(self.__url)

            list_button = self.__driver.find_element(by=By.XPATH, value=self.__list_button_path)
            list_button.click()

            spec_input = self.__driver.find_element(by=By.XPATH, value=self.__spec_input_path)
            spec_input.send_keys(speciality)

            select_spec = self.__driver.find_element(
                    by=By.XPATH, value=self.__select_spec_path
                ).find_element(
                    by=By.CLASS_NAME, value='active'
                ).find_element(
                    by=By.CLASS_NAME, value='active'
                )
            self.__driver.execute_script("arguments[0].click();", select_spec)

            self.__driver.find_element(by=By.ID, value=self.__search_button_id).click()

            unis = self.__driver.find_element(by=By.ID, value=self.__university_id)
            for uni in unis.find_elements(by=By.CLASS_NAME, value=self.__university_cl):
                uni.click()
                print(uni.text, end='\n\n')

            func(self)

            self.__driver.quit()
        
        return wrapper

    @__interact
    def get_data(self) -> list:
        pass

i = Interaction()

print(i.get_data('122'))
#spec = 122
#with open(f'page_source/{spec}.html', 'w') as file:
#    file.write(i.get_source(spec))