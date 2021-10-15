from django.db.models import fields
from rest_framework import serializers, exceptions
from .models import Task
from users.models import User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "task_title", "task_description", "user_id", "issued_on", "done_at", "task_type"]


    
    def validate(self, attrs):
        super().validate(attrs)
        if(attrs["task_type"] == Task._done_task):
            raise exceptions.ValidationError("cannot post a done task")
        return attrs



