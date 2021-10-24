from django.db import models
from users.models import User
# Create your models here.



class Task(models.Model):
    _pending_task = 0
    _done_task = 1
    _lazy_task = 2

    TASK_TYPES = (
        (_pending_task , "pending_task"),
        (_done_task, "done_task"),
        (_lazy_task, "lazy_task")
    )

    task_description = models.CharField(max_length= 500)
    task_title = models.CharField(max_length= 100)
    user_id = models.ForeignKey(to = User, related_name= "tasks", on_delete= models.CASCADE)
    issued_on = models.DateTimeField(auto_now= True)
    task_deadline = models.DateTimeField()
    done_at = models.DateTimeField(blank= True, null= True)
    task_type = models.SmallIntegerField(choices= TASK_TYPES)

