from django.conf import settings
from celery.result import AsyncResult
from django.http import JsonResponse
from webparser.data.parsing import Parser
from webparser.options.models import Region

def check_parse(request, id: str):

    # check the task status
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        
        # the task is complete, return the result
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

        # for region in regions:
        #     print(f'\n\n{region}\n\n')

        return JsonResponse({'status': 'SUCCESS', 'result': regions, 'shorts': []})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        # the task is still running
        return JsonResponse({'status': task.state})
    else:
        # the task failed
        return JsonResponse({'status': 'FAILURE', 'result': task.result})