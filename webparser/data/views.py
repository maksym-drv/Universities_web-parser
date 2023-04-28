from celery.result import AsyncResult
from django.http import JsonResponse
from .report import Report as rprt
from django.views import View
from accounts.models import CustomUser
from django.core.files import File

class TaskView(View):

    def post(self, request, id: int):

        task = AsyncResult(id)
        if task.state == 'SUCCESS':
            regions: list = task.result

            if task.name == 'info':
                pass
                
                # file_path = rprt.static_data(1, regions)
                # with open(file_path, 'rb') as f:
                #     file = File(f)
                #     user: CustomUser = request.user
                #     user.short_table.delete()
                #     user.short_table.save('static.xlsx', file, save=True)
                #     user.save()
                # rprt.delete(file_path)

                file_path = rprt.short_data(regions, 'short', task.id)
                with open(file_path, 'rb') as f:
                    file = File(f)
                    user: CustomUser = request.user
                    user.short_table.delete()
                    user.short_table.save('short.xlsx', file, save=True)
                    user.save()
                rprt.delete(file_path)
                
            return JsonResponse({'status': 'SUCCESS', 'result': regions, 'shorts': []})
        elif task.state == 'PENDING' or task.state == 'STARTED':
            return JsonResponse({'status': task.state})
        else:
            return JsonResponse({'status': 'FAILURE', 'result': task.result})