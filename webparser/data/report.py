from os import path, remove
import pandas as pd
from django.conf import settings

class Report:

    def __init__(self, regions: list) -> None:
        self.regions = regions
    
    def get_file(sort_table):
        def wrapper(self, name: str, id: str, last_column: str = 'H') -> str:

            regions = self.regions
            file_name = f'{name}_{id}.xlsx'
            file_path = path.join(settings.MEDIA_ROOT, file_name)
            writer = pd.ExcelWriter(file_path)

            yellow_format = writer.book.add_format({'bg_color': 'yellow', 'border': 1})
            gray_format = writer.book.add_format({'bg_color': 'gray', 'border': 1})

            for region in regions:

                _table = sort_table(self, region[name])        

                df = pd.DataFrame(_table)

                df.to_excel(writer, index=False, 
                    sheet_name = region['name'])
                
                size = f'A2:{last_column}{df.shape[0] + 1}'
                worksheet = writer.sheets[region['name']]

                worksheet.conditional_format(size, {'type': 'blanks',
                                                'format': gray_format})
                worksheet.conditional_format(size, {'type': 'no_blanks',
                                                'format': yellow_format})
                worksheet.autofit()

            writer.close() 

            return file_path
        return wrapper
    
    @get_file
    def static_data(self, region_static: list):

        region = {}

        for _name in 'Назва закладу освіти', 'Назва пропозиції', \
            'Спеціальність', 'Форма навчання', 'Кількість заяв', \
            'Зараховано (бюджет)', 'Зараховано (контракт)', \
            'Вартість навчання':
            region[_name] = []

        for uni in region_static:
            uni: dict

            region["Назва закладу освіти"].append(uni['name'])
            region["Назва закладу освіти"].extend(
                ['' for _offer in uni['offers'][1:]]
            )

            for offer in uni['offers']:
                offer: dict

                region['Назва пропозиції'].append(offer['name'])
                region['Спеціальність'].append(offer['id'])
                region['Форма навчання'].append(offer['form'])
                region['Кількість заяв'].append(offer['apps'])
                region['Зараховано (бюджет)'].append(offer['ob'])
                region['Зараховано (контракт)'].append(offer['oc'])
                region['Вартість навчання'].append(offer['price'])

            for _name in region.keys():
                region[_name].append('')

        return region
    
    @get_file
    def short_data(self, region_short: list):

        region = {}

        for _name in 'Спеціальність', 'Форма навчання', 'Кількість заяв', \
            'Зараховано (бюджет)', 'Зараховано (контракт)', 'Всього', \
            'Вартість навчання (мін.)', 'Вартість навчання (макс.)':
            region[_name] = []

        for _data in region_short:
            _data: dict

            region['Спеціальність'].extend(
                [_data['name'], '', '', '']
            )
            region['Форма навчання'].extend(
                ['Денна', 'Заочна', 'Всього:', '']
            )
            region['Кількість заяв'].extend([
                _data['fulltime_apps'],
                _data['parttime_apps'],
                _data['apps'], ''
            ])
            region['Зараховано (бюджет)'].extend([
                _data['fulltime_budget'],
                _data['parttime_budget'],
                _data['budget'], ''
            ])
            region['Зараховано (контракт)'].extend([
                _data['fulltime_contract'],
                _data['parttime_contract'],
                _data['contract'], ''
            ])
            region['Всього'].extend([
                _data['fulltime'],
                _data['parttime'],
                _data['enrolled'], ''
            ])
            region['Вартість навчання (мін.)'].extend([
                _data['min_fulltime'],
                _data['min_parttime'],
                '', ''
            ])
            region['Вартість навчання (макс.)'].extend([
                _data['max_fulltime'],
                _data['max_parttime'],
                '', ''
            ])

        return region
    
    @get_file
    def programs_data(self, region_static: list):

        region = {}

        for _name in 'Назва закладу освіти', 'Освітня програма':
            region[_name] = []

        for uni in region_static:
            uni: dict

            region["Назва закладу освіти"].append(uni['name'])
            region["Назва закладу освіти"].extend(
                ['' for _programs in uni['programs'][1:]]
            )
            region["Освітня програма"].extend(uni['programs'])

            for _name in region.keys():
                region[_name].append('')

        return region
        
    @staticmethod
    def delete(file_path: str):
        remove(file_path)
