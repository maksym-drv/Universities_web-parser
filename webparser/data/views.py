from requests import get
from django.conf import settings
from celery.result import AsyncResult
from django.http import JsonResponse
from webparser.options.models import Region

def check_parse(request, id: str):

    # check the task status
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        
        # the task is complete, return the result
        unis = task.result
        regions = []

        response = get(settings.UNIVERSITIES_URL, 
                    params=settings.DEFAULT_PARAMS)
        all_unis: list = response.json()
        
        for uni in unis:
            
            region_name = next((_uni['region_name_u'] for _uni in all_unis 
                        if _uni['university_id'] == uni['id']), None)
            
            region_index = next((index for (index, _region) in enumerate(regions) 
                    if _region['name'] == region_name), None)
            
            if isinstance(region_index, int):
                regions[region_index]['unis'].append(uni)
            else:
                _region = {}
                _region['id'] = Region.objects.get(name = region_name).registry_id
                _region['name'] = region_name
                _region['unis'] = []
                _region['unis'].append(uni)
                regions.append(_region)

        return JsonResponse({'status': 'SUCCESS', 'result': regions})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        # the task is still running
        return JsonResponse({'status': task.state})
    else:
        # the task failed
        return JsonResponse({'status': 'FAILURE', 'result': task.result})