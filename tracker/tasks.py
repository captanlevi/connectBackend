from celery import shared_task
from django.utils import timezone
from .models import Task
from typing import List
  
@shared_task(name='move_to_lazy')
def moveToLazy():
  pending_tasks : List[Task] = list(Task.objects.filter(task_type = Task._pending_task))
  for pending_task in pending_tasks:
      if(pending_task.task_deadline < timezone.now()):
          print("moving")
          pending_task.task_type = Task._lazy_task
          pending_task.save()