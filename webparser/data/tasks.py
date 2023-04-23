#from multiprocessing.dummy import Pool
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from .scraping import Scraper
from celery import shared_task
from django.conf import settings
from webparser.options.models import Region

@shared_task
def info_task(specialities: list,
                unis: list,
                qualification: str,
                education_base: str):

    scraper = Scraper(
        unis = unis,
        url = settings.TARGET_URL,
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
    shorts = []

    for region in Region.objects.all():

        if not unis: break

        _region = {}
        _region['id'] = region.registry_id
        _region['name'] = region.name
        _region['unis'] = []

        params: dict = settings.DEFAULT_PARAMS.copy()
        params['lc'] = region.registry_id
        region_unis: list = Scraper.get_json(
            settings.UNIVERSITIES_URL, 
            params=params
        )

        for uni in unis:

            if next((True for region_uni in region_unis 
                if region_uni['university_id'] == uni['id']), 
                False):
                    
                uni_index = next(
                    (index for (index, _uni) in enumerate(_region['unis'])
                    if _uni['id'] == uni['id']), None)

                if isinstance(uni_index, int):
                    _region['unis'][uni_index]['offers'] += uni['offers']
                else:
                    _uni = {}
                    _uni['id'] = uni['id']
                    _uni['name'] = uni['name']
                    _uni['offers'] = []
                    _uni['offers'] += uni['offers']
                    _region['unis'].append(_uni)

        for uni in region_unis:
            found_unis = [_uni for _uni in unis 
                if _uni['id'] == uni['university_id']]
            for found_uni in found_unis:
                unis.remove(found_uni)

        if _region['unis']:
            regions.append(_region)

    return regions

@shared_task
def regions_task(saved_unis: list = []):
    
    regions = []
    
    for region in Region.objects.all():

        _region = {}
        _region['id'] = region.id
        _region['name'] = region.name

        params: dict = settings.DEFAULT_PARAMS.copy()
        params['lc'] = region.registry_id

        unis: list = Scraper.get_json(
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