from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.serializers import Serializer 


from .serializers import TaskSerializer
from .models import Task
from users.models import User

# Create your views here.



@api_view(["POST", "GET"])
def taskView(request : Request):
    if(request.method == "GET"):
        user = request.user
        all_objects = Task.objects.filter(user_id = user.id)
        serializer = TaskSerializer(instance= all_objects, many = True)
        return Response(serializer.data)

    if(request.method == "POST"):
        serializer = TaskSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def taskSpecificView(request,id : int):
    if(request.method == "GET"):
        try:
            instance = Task.objects.get(id = id)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError("task with id {} does not exists".format(id))

        serializer = TaskSerializer(instance= instance)
        return Response(serializer.data, status= status.HTTP_200_OK)