from multiprocessing.dummy import Pool
from .scraping import Scraper
from celery import shared_task
from django.conf import settings

@shared_task
def create_task(specialities: list,
                unis: list,
                qualification: str,
                education_base: str):
    
    print('im starting task!')

    parser = Scraper(
        unis = unis,
        url = settings.TARGET_URL,
        executable_path = settings.EXECUTABLE_PATH,
        firefox_options = settings.FIREFOX_OPTIONS,
        qualification = qualification,
        education_base = education_base
    )

    print('im in the task')

    with Pool(len(specialities)) as p:
        spec_unis = p.map(parser.get_uni_data, specialities)

    unis = []

    for spec_uni in spec_unis:
        for uni in spec_uni:
            uni_index = next((index for (index, _uni) in enumerate(unis) 
                            if _uni['id'] == uni['id']), None)
            
            if isinstance(uni_index, int):
                unis[uni_index]['offers'] += uni['offers']
            else:
                _uni = {}
                _uni['id'] = uni['id']
                _uni['name'] = uni['name']
                _uni['offers'] = []
                _uni['offers'] += uni['offers']
                unis.append(_uni)

    return unis