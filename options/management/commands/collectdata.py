from django.core.management.base import BaseCommand, CommandError
from options.models import Region, Speciality
from urllib.error import URLError
from django.conf import settings
import pandas as pd

class Command(BaseCommand):
    help = 'Collect specialities data.'

    def handle(self, *args, **kwargs):

        region_id = 'Код регіону'
        region_name = 'Назва регіону'
        speciality_id = 'Код спеціальності'
        speciality_name = 'Назва спеціальності'
        
        try:
            regions = pd.read_excel(settings.REGIONS_URL)
            specialities = pd.read_excel(settings.SPECIALITIES_URL)
        except URLError:
            raise CommandError('Cannot connect to the server.')
        
        for index, region in enumerate(regions[region_id]):

            region = Region(
                name = regions[region_name][index],
                registry_id = regions[region_id][index]
            )
            region.save()

        for index, speciality in enumerate(specialities[speciality_id]):

            speciality = Speciality(
                name = specialities[speciality_name][index],
                registry_id = specialities[speciality_id][index]
            )
            speciality.save()

        self.stdout.write(self.style.SUCCESS("Specialities data saved!"))