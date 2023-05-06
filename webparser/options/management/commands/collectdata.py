from django.core.management.base import BaseCommand, CommandError
from webparser.options.models import Region, Speciality
from webparser.data.scraping import Scraper
from urllib.error import URLError
from django.conf import settings

class Command(BaseCommand):
    help = 'Collect specialities data.'

    def handle(self, *args, **kwargs):
        
        try:
            regions = Scraper.get_table(settings.REGIONS_URL)
            specialities = Scraper.get_page(settings.TARGET_URL())
        except URLError:
            raise CommandError('Cannot connect to the server.')
        
        for region in Scraper.get_region_options(regions):
            Region.objects.get_or_create(**region)

        for speciality in Scraper.get_speciality_options(specialities):
            Speciality.objects.get_or_create(**speciality)

        self.stdout.write(self.style.SUCCESS("Data saved!"))