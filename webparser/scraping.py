from bs4 import BeautifulSoup
from .parsing import Parser

class Scraper(Parser):

    def get_uni_data(self, speciality: str) -> str:

        raw_data = self.get_raw_uni(speciality)

        def get_offer_data(soup: BeautifulSoup, class_name: str):
            offer = soup.find('dl', {'class': class_name})
            if not offer: return
            return offer.find('dd').text
        
        def get_stat_data(soup: BeautifulSoup, class_name: str):
            if not soup: return 0
            stat = soup.find('div', {'class': class_name})
            if not stat: return 0
            return stat.find('div', {'class': 'value'}).text

        soup = BeautifulSoup(raw_data, 'html.parser')

        unis_soup = soup.find('div', id='universities')

        data = []

        for uni in unis_soup.find_all('div', {'class': 'university'}):

            uni_id = f"{uni['data-university']}"
            _uni = {}
            _uni['id'] = uni_id
            _uni['name'] = \
                uni.find('h5', {'class': 'text-primary text-uppercase'}).text
            
            for offer in uni.find_all('div', {'class': 'offer'}):
                
                _uni['offer'] = {}

                offer_name = offer.find_all(
                    'dl', 
                    {'class': 'offer-university-specialities-name'}
                )[1]
                _uni['offer']['name'] = offer_name.find('dd').text
                
                form = get_offer_data(offer, 'row offer-education-form-name')
                if form: 
                    _uni['offer']['form'] = form
                
                price = get_offer_data(offer, 'row offer-education-price')
                if price: 
                    _uni['offer']['price'] = price
                
                statistics = offer.find('div', {'class': 'offer-requests-stats'})

                applications = get_stat_data(statistics, 'stats-field-t')
                if applications:
                    _uni['offer']['applications'] = applications
                
                ob = get_stat_data(statistics, 'stats-field-ob')
                if ob: _uni['offer']['ob'] = ob
                
                oc = get_stat_data(statistics, 'stats-field-oc')
                if oc: _uni['offer']['oc'] = oc

            data.append(_uni)
                
        return data