from time import sleep
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

specialities = ['122', '123']

class Interaction:
    list_button_path    = '//*[@id="search-form-general"]/div[2]/div/div[1]/button'
    spec_input_path     = '/html/body/div[2]/div/div[1]/input'
    select_spec_path    = '//*[@id="bs-select-3"]/ul'
    search_button_id    = 'offers-search-button'
    universitis_id      = 'universities'
    universitis_cl      = 'university'
    
    def __init__(self, url: str = 'https://vstup.edbo.gov.ua/offers/') -> None:
        options = webdriver.FirefoxOptions()
        options.binary_location = r'/Applications/Firefox.app/Contents/MacOS/firefox'
        self.__driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.__url = url
        sleep(1)

    def get_source(self, speciality: str) -> str:

        self.__driver.get(self.__url)

        list_button = self.__driver.find_element(by=By.XPATH, value=self.list_button_path)
        list_button.click()

        spec_input = self.__driver.find_element(by=By.XPATH, value=self.spec_input_path)
        spec_input.send_keys(speciality)

        select_spec = self.__driver.find_element(
                by=By.XPATH, value=self.select_spec_path
            ).find_element(
                by=By.CLASS_NAME, value='active'
            ).find_element(
                by=By.CLASS_NAME, value='active'
            )
        self.__driver.execute_script("arguments[0].click();", select_spec)
    
        self.__driver.find_element(by=By.ID, value=self.search_button_id).click()

        unis = self.__driver.find_element(by=By.ID, value=self.universitis_id)
        for uni in unis.find_elements(by=By.CLASS_NAME, value=self.universitis_cl):
            uni.click()

        page_source = self.__driver.page_source

        self.__driver.quit()

        return page_source

i = Interaction()
spec = 122
with open(f'page_source/{spec}.html', 'w') as file:
    file.write(i.get_source(spec))