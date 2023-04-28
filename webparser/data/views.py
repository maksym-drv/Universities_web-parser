from django.views import View
from django.core.files import File
from django.http import JsonResponse
from celery.result import AsyncResult
from webparser.templates.models import Template
from .report import Report as rprt

class TaskView(View):

    def post(self, request, id: int):

        task = AsyncResult(id)
        if task.state == 'SUCCESS':
            
            result: dict = {}
            files: list = []
            regions: list = task.result

            if task.name == 'info' \
                and request.POST.get('template'):

                tmplt = Template.objects.get(id = request.POST['template'])
            
                file_path = rprt.static_data(regions, 'static', task.id)
                with open(file_path, 'rb') as f:
                    file = File(f)
                    tmplt.static_table.delete()
                    tmplt.static_table.save('static.xlsx', file, save=True)
                    tmplt.save()
                rprt.delete(file_path)

                report = {
                    'text': 'Завантажити статистичні дані',
                    'url': tmplt.static_table.url
                }
                files.append(report)

                file_path = rprt.short_data(regions, 'short', task.id)
                with open(file_path, 'rb') as f:
                    file = File(f)
                    tmplt.short_table.delete()
                    tmplt.short_table.save('short.xlsx', file, save=True)
                    tmplt.save()
                rprt.delete(file_path)

                report = {
                    'text': 'Завантажити зведені дані',
                    'url': tmplt.short_table.url
                }
                files.append(report)

                result['files'] = files

            result['regions'] = regions
                
            return JsonResponse({'status': 'SUCCESS', 'result': result})
        elif task.state == 'PENDING' or task.state == 'STARTED':
            return JsonResponse({'status': task.state})
        else:
            return JsonResponse({'status': 'FAILURE', 'result': task.result})