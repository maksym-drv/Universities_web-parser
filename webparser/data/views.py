from celery.result import AsyncResult
from django.http import JsonResponse

def check(request, id: str):

    # check the task status
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        regions: list = task.result
        return JsonResponse({'status': 'SUCCESS', 'result': regions, 'shorts': []})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        return JsonResponse({'status': task.state})
    else:
        return JsonResponse({'status': 'FAILURE', 'result': task.result})