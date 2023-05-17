#from multiprocessing.dummy import Pool
#from threading import Thread
from .parsing import Parser
from .scraping import Scraper
from celery import shared_task
from django.conf import settings
from webparser.options.models import Region
from concurrent.futures import ThreadPoolExecutor

@shared_task(name='info')
def info_task(specialities: list,
            unis: list,
            year: int,
            qualification: str,
            education_base: str) -> list:

    scraper = Scraper(
        unis = unis,
        url = settings.TARGET_URL(year),
        executable_path = settings.EXECUTABLE_PATH,
        firefox_options = settings.FIREFOX_OPTIONS,
        qualification = qualification,
        education_base = education_base
    )

    # with Pool(len(specialities)) as p:
    #     spec_unis = p.map(parser.get_uni_data, specialities)
    
    with ThreadPoolExecutor(max_workers=len(specialities)) as executor:
        raw_unis = executor.map(scraper.get_raw_unis, specialities)
        spec_unis = executor.map(scraper.get_uni_data, raw_unis)

    unis = [uni for spec_uni in spec_unis for uni in spec_uni]

    regions = []

    for region in Region.objects.all():

        if not unis: break

        _region = {}
        _region['id'] = region.registry_id
        _region['name'] = region.name

        params: dict = settings.DEFAULT_PARAMS.copy()
        params['lc'] = region.registry_id
        region_unis: list = Scraper.get_abstract_json(
            settings.UNIVERSITIES_URL, 
            params=params
        )

        parser = Parser()
        _region['static'] = parser.get_static_table(
            unis,
            region_unis
        )
        _region['short'] = parser.short_tables

        for uni in region_unis:
            found_unis = [_uni for _uni in unis 
                if _uni['id'] == uni['university_id']]
            for found_uni in found_unis:
                unis.remove(found_uni)

        if _region['static']:
            regions.append(_region)

    return regions

@shared_task(name='regions')
def regions_task(saved_unis: list = []) -> list:
    
    regions = []
    
    for region in Region.objects.all():

        _region = {}
        _region['id'] = region.id
        _region['name'] = region.name

        params: dict = settings.DEFAULT_PARAMS.copy()
        params['lc'] = region.registry_id

        unis: list = Scraper.get_abstract_json(
            settings.UNIVERSITIES_URL, 
            params=params
        )
        
        if saved_unis:
            for uni in unis:
                if uni['university_id'] in saved_unis:
                    uni['checkbox'] = True

        _region['unis'] = unis

        if _region['unis']:
            regions.append(_region)

    return regions