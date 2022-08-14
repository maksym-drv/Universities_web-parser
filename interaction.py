from time import sleep
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

specialities = ['122', '123']

options = webdriver.FirefoxOptions()
options.binary_location = r'/Applications/Firefox.app/Contents/MacOS/firefox'

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

driver.get('https://vstup.edbo.gov.ua/offers/')

sleep(1)

list_button = driver.find_element(by=By.XPATH, value='//*[@id="search-form-general"]/div[2]/div/div[1]/button')

for speciality in specialities:

    list_button.click()

    spec_input = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]/input')
    spec_input.send_keys(speciality)

    current_spec = driver.find_element(
            by=By.XPATH, value='//*[@id="bs-select-3"]/ul'
        ).find_element(
            by=By.CLASS_NAME, value='active'
        ).find_element(
            by=By.CLASS_NAME, value='active'
        )
    driver.execute_script("arguments[0].click();", current_spec)
    
    driver.find_element(by=By.ID, value='offers-search-button').click()

    unis = driver.find_element(by=By.ID, value='universities')
    for uni in unis.find_elements(by=By.CLASS_NAME, value='university'):
        uni.click()

    with open(f'page_source/{speciality}.html', 'w') as file:
        file.write(driver.page_source)