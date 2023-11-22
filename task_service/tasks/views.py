from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Task
from .serializers import TaskSerializer
# from .tasks import receive_task


@method_decorator(csrf_exempt, name='dispatch')
class TaskView(View):
    def post(self, request, *args, **kwargs):
        data = {
            'number': request.POST.get('number'),
            'status': 'created',
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # receive_task.delay(serializer.data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({'error': 'Invalid data'}, status=400)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)
