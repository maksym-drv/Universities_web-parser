from django.core.management.base import BaseCommand, CommandError
from webparser.options.models import Region, Speciality
from urllib.request import urlopen
from urllib.error import URLError
from django.conf import settings
from bs4 import BeautifulSoup
import pandas as pd

class Command(BaseCommand):
    help = 'Collect specialities data.'

    def handle(self, *args, **kwargs):

        region_id = 'Код регіону'
        region_name = 'Назва регіону'

        speciality_id = 'offers-search-speciality'
        
        try:
            regions = pd.read_excel(settings.REGIONS_URL)
            file = urlopen(settings.TARGET_URL)
        except URLError:
            raise CommandError('Cannot connect to the server.')
        
        for index, region in enumerate(regions[region_id]):

            region = Region(
                name = regions[region_name][index],
                registry_id = regions[region_id][index]
            )
            region.save()

        soup = BeautifulSoup(file.read(), 'html.parser')
        select = soup.find(
            "select", 
            { "id": speciality_id }
        )

        for option in select.find_all('option'):

            option: BeautifulSoup
            speciality_id = option.get('value')
            if not speciality_id: continue

            speciality = Speciality(
                name = option.text,
                registry_id = speciality_id
            )
            speciality.save()

        self.stdout.write(self.style.SUCCESS("Specialities data saved!"))