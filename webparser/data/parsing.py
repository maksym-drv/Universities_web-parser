from webparser.options.models import Speciality

class Parser:

    def __init__(self):
        self.__short_tables = []

    def __add_short_table(self, offer: dict) -> int:

        _spec = {}
        _spec['id'] = offer['id']
        _spec['name'] = Speciality.objects.get(
            registry_id = offer['id']
        ).name

        for _name in ('fulltime_apps', 'parttime_apps', 'apps', 
                    'fulltime_budget', 'fulltime_contract', 
                    'parttime_budget',  'parttime_contract',
                    'budget', 'contract', 'enrolled', ):
            _spec[_name] = 0
        
        _spec['fulltime_prices'] = []
        _spec['parttime_prices'] = []

        self.__short_tables.append(_spec)
        return self.__short_tables.index(_spec)

    def __update_short_table(self, offers: list):

        for offer in offers:
            offer: dict

            spec_index = next(
            (index for (index, _spec) in enumerate(self.__short_tables)
            if _spec['id'] == offer['id']), None)

            if not isinstance(spec_index, int):
                spec_index = self.__add_short_table(offer)

            spec = self.__short_tables[spec_index]

            spec['fulltime_apps'] += offer['apps'] if \
                offer['form'] == 'Денна' else 0
            spec['parttime_apps'] += offer['apps'] if \
                offer['form'] == 'Заочна' else 0
            spec['fulltime_budget'] += offer['ob'] if \
                offer['form'] == 'Денна' else 0
            spec['fulltime_contract'] += offer['oc'] if \
                offer['form'] == 'Денна' else 0
            spec['parttime_budget'] += offer['ob'] if \
                offer['form'] == 'Заочна' else 0
            spec['parttime_contract'] += offer['oc'] if \
                offer['form'] == 'Заочна' else 0
            
            spec['apps'] = spec['fulltime_apps'] + spec['parttime_apps']
            spec['budget'] = spec['fulltime_budget'] + spec['parttime_budget']
            spec['contract'] = spec['fulltime_contract'] + spec['parttime_contract']
            spec['fulltime'] = spec['fulltime_budget'] + spec['fulltime_contract']
            spec['parttime'] = spec['parttime_budget'] + spec['parttime_contract']
            spec['enrolled'] = spec['budget'] + spec['contract']

            _price = (lambda _name: offer[_name] if isinstance(
                offer.get(_name), int) else None)('price')

            if _price:
                if offer['form'] == 'Денна':
                    spec['fulltime_prices'].append(_price)
                elif offer['form'] == 'Заочна':
                    spec['parttime_prices'].append(_price)
    

    def get_static_table(self, unis: list, 
                   region_unis: list) -> list:
        
        static_tables = []

        for uni in unis:

            if next((True for region_uni in region_unis 
                if region_uni['university_id'] == uni['id']), 
                False):

                self.__update_short_table(uni['offers'])
                
                programs = set([offer['program'] \
                            for offer in uni['offers']])
                        
                uni_index = next(
                    (index for (index, _uni) in enumerate(static_tables)
                    if _uni['id'] == uni['id']), None)

                if isinstance(uni_index, int):
                    static_tables[uni_index]['offers'] += uni['offers']
                    static_tables[uni_index]['programs'] += list(programs)
                else:
                    _uni = {}
                    _uni['id'] = uni['id']
                    _uni['name'] = uni['name']
                    _uni['offers'] = []
                    _uni['offers'] += uni['offers']
                    _uni['programs'] = []
                    _uni['programs'] += list(programs)
                    static_tables.append(_uni)

        return static_tables
    
    @property
    def short_tables(self):

        def get_value(data: list, func):
            try:
                return func(data)
            except ValueError:
                return 0
            
        for spec in self.__short_tables:

            spec: dict
            fulltime_prices = spec.pop('fulltime_prices')
            parttime_prices = spec.pop('parttime_prices')
            
            spec['max_fulltime'] = get_value(fulltime_prices, max)
            spec['max_parttime'] = get_value(parttime_prices, max)
            spec['min_fulltime'] = get_value(fulltime_prices, min)
            spec['min_parttime'] = get_value(parttime_prices, min)

        return self.__short_tables
    
    @staticmethod
    def get_region_options(raw_regions) -> list:

        region_id = 'Код регіону'
        region_name = 'Назва регіону'
        data = []

        for index, region in enumerate(raw_regions[region_id]):

            data.append({
                'name': raw_regions[region_name][index],
                'registry_id': raw_regions[region_id][index]
            })
        
        return data
