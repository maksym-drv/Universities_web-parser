from requests import get
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

class Unprotector:

    university_id       = 'universities'
    university_class    = 'university'

    def __init__(self, url: str, executable_path: str,
                firefox_options: FirefoxOptions, 
                qualification: str, education_base: str) -> None:

        self.url = url
        self.executable_path = executable_path
        self.firefox_options = firefox_options

        self.options = {
            'qualification': qualification,
            'education_base': education_base
        }

    def get_raw_unis(self, speciality: str) -> str:

        driver = Firefox(
            executable_path = self.executable_path, 
            options         = self.firefox_options,
        )

        self.options['speciality'] = speciality

        url = get(self.url, params=self.options).url
        driver.get(url)
        
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, self.university_class)))
        except TimeoutException:
            return None

        unis = driver.find_element(by=By.ID, value = self.university_id)

        for uni in unis.find_elements(by=By.CLASS_NAME, value = self.university_class):
            uni.click()

        raw_page = driver.page_source

        driver.quit()

        return raw_page
