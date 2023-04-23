from django.conf import settings
from celery.result import AsyncResult
from django.http import JsonResponse
from webparser.data.parsing import Parser
from webparser.options.models import Region

def check_info(request, id: str):

    # check the task status
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        
        unis: list = task.result
        regions = []
        shorts = []

        for region in Region.objects.all():

            if not unis: break
            
            params: dict = settings.DEFAULT_PARAMS.copy()
            params['lc'] = region.registry_id
            region_unis: list = Parser.get_json(
                settings.UNIVERSITIES_URL, 
                params=params
            )

            _region = {}
            _region['id'] = region.registry_id
            _region['name'] = region.name
            _region['unis'] = [uni for uni in unis 
                                if next((True for region_uni in region_unis 
                                if region_uni['university_id'] == uni['id']), 
                                False)]

            for uni in _region['unis']:
                unis.remove(uni)
            
            if _region['unis']:
                regions.append(_region)

        return JsonResponse({'status': 'SUCCESS', 'result': regions, 'shorts': []})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        return JsonResponse({'status': task.state})
    else:
        return JsonResponse({'status': 'FAILURE', 'result': task.result})
    

def check_regions(request, id: str):

    # check the task status
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        regions: list = task.result
        return JsonResponse({'status': 'SUCCESS', 'result': regions, 'shorts': []})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        return JsonResponse({'status': task.state})
    else:
        return JsonResponse({'status': 'FAILURE', 'result': task.result})