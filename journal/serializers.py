from django.utils import timezone
from rest_framework import fields, serializers, exceptions
from rest_framework.fields import SerializerMethodField
from .models import Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta():
        model = Journal
        fields = ["id", "title", "date", "message", "user_id"]


    def validate(self, attrs):
        super().validate(attrs)
        #if(attrs["date"] > timezone.now()):
        #   raise exceptions.ValidationError("date time cannot be something in the future.")

        return attrs