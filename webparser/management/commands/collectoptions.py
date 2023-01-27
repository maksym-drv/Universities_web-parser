from django.core.management.base import BaseCommand, CommandError
from urllib.error import URLError
from django.conf import settings
from bs4 import BeautifulSoup
from urllib.request import urlopen
from json import dump

class Command(BaseCommand):
    help = 'Collect parser options in a single location.'

    def handle(self, *args, **kwargs):

        options = {}
        
        try:
            response = urlopen(settings.TARGET_URL)
        except URLError:
            raise CommandError('Cannot connect to the server.')

        file = BeautifulSoup(response.read(), 'html.parser')

        for target_option in settings.TARGET_OPTIONS:
           
            select = file.find(
                "select", 
                { "id": settings.TARGET_OPTIONS[target_option] }
            )

            data = []
            for _option in select.find_all('option'):
                _option: BeautifulSoup
                value = _option.get('value')
                if value: data.append(( value, _option.find(text=True ) ))
            
            options[target_option] = data
    
        for option in options:
            with open(f'{settings.OPTIONS_ROOT}/{option}.json', 'w') as file:
                dump(options[option], file, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f"Parser options saved to '{settings.OPTIONS_ROOT}'."))