from webparser.options.models import Speciality

class Sorter:

    def __init__(self):
        self.short_tables = []
        self.programs_table = []

    def __add_short_table(self, offer: dict) -> int:

        _spec = {}
        _spec['id'] = offer['id']
        _spec['name'] = Speciality.objects.get(
            registry_id = offer['id']
        ).name

        for _name in ('fulltime_apps', 'parttime_apps', 'apps', 
                    'fulltime_budget', 'fulltime_contract', 'budget',
                    'parttime_budget', 'parttime_contract', 'contract',
                    'enrolled', 'max_fulltime', 'min_fulltime',
                    'max_parttime', 'min_parttime', ):
            _spec[_name] = 0

        self.short_tables.append(_spec)
        return self.short_tables.index(_spec)

    def __update_short_table(self, offers: list):

        for offer in offers:
            offer: dict

            spec_index = next(
            (index for (index, _spec) in enumerate(self.short_tables)
            if _spec['id'] == offer['id']), None)

            if not isinstance(spec_index, int):
                spec_index = self.__add_short_table(offer)

            spec = self.short_tables[spec_index]

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
                offer.get(_name), int) else 0)('price')

            spec['max_fulltime'] = offer['price'] if \
                offer['form'] == 'Денна' and \
                _price > int(spec['max_fulltime']) \
                    else int(spec['max_fulltime'])
            
            spec['max_parttime'] = offer['price'] if \
                offer['form'] == 'Заочна' and \
                _price > int(spec['max_parttime']) \
                    else int(spec['max_parttime'])
            
            spec['min_fulltime'] = offer['price'] if \
                offer['form'] == 'Денна' and \
                _price < int(spec['min_fulltime']) \
                or spec['min_fulltime'] == 0 else int(spec['min_fulltime'])

            spec['min_parttime'] = offer['price'] if \
                offer['form'] == 'Заочна' and \
                _price < int(spec['min_parttime']) \
                or spec['min_parttime'] == 0 else int(spec['min_parttime'])

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