from requests import get
from django.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class Parser:

    university_id       = 'universities'
    university_class    = 'university'

    url = settings.TARGET_URL

    def __init__(self, **options) -> None:

        self.options = options

    def get_universities(self):

        driver = settings.WEB_DRIVER

        url = get(url, params=self.options).url
        driver.get(url)
        
        wait = WebDriverWait(driver, 200)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, self.university_class)))

        unis = driver.find_element(by=By.ID, value = self.university_id)
        for uni in unis.find_elements(by=By.CLASS_NAME, value = self.university_class):
            uni.click()

        self.page_source = driver.page_source
