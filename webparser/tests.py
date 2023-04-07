from django.test import TestCase
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from scraping import Scraper

from multiprocessing.dummy import Pool
from time import time
from json import dump

# Create your tests here.

TARGET_URL = 'https://vstup.edbo.gov.ua/offers/'

FIREFOX_OPTIONS = FirefoxOptions()
FIREFOX_OPTIONS.add_argument('--headless')
FIREFOX_OPTIONS.add_argument('--mute-audio')
FIREFOX_OPTIONS.add_argument('--no-sandbox')
FIREFOX_OPTIONS.add_argument('--disable-dev-shm-usage')
EXECUTABLE_PATH = GeckoDriverManager().install()

parser = Scraper(
    url = TARGET_URL,
    executable_path = EXECUTABLE_PATH,
    firefox_options = FIREFOX_OPTIONS,
    qualification = '1',
    education_base = '40'
)

specialities = ['122', '123', '124']

start_time = time()

with Pool(len(specialities)) as p:
    spec_unis = p.map(parser.get_uni_data, specialities)

# spec_unis = []
# for spec in specialities:
#     spec_unis.append(parser.get_uni_data(spec))

unis = []

for spec_uni in spec_unis:
    for uni in spec_uni:
        uni_index = next((index for (index, _uni) in enumerate(unis) 
                        if _uni['id'] == uni['id']), None)
        
        if isinstance(uni_index, int):
            unis[uni_index]['offers'].append(uni['offer'])
        else:
            _uni = {}
            _uni['id'] = uni['id']
            _uni['name'] = uni['name']
            _uni['offers'] = []
            _uni['offers'].append(uni['offer'])
            unis.append(_uni)

end_time = time()

with open('data.json', 'w') as file:
    dump(unis, file, ensure_ascii=False)

print(f'TIME === {end_time - start_time}')