from django.shortcuts import render
from rest_framework import exceptions, serializers
from .models import Journal
from .serializers import JournalSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@api_view(["GET", "POST"])
def journalView(request):
    if(request.method == "GET"):
        journals = Journal.objects.all()
        serializer = JournalSerializer(journals, many = True)
        return Response(serializer.data)

    if(request.method == "POST"):
        serializer = JournalSerializer(data = request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def journalViewByID(request, id : int):
    if(request.method == "GET"):
        try:
            journalInstance = Journal.objects.get(id = id)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError("journal with id {} does not exist".format(id))

        serializer = JournalSerializer(instance=journalInstance)
        return Response(serializer.data)

