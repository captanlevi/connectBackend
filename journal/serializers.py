from datetime import datetime
from rest_framework import fields, serializers, exceptions
from rest_framework.fields import SerializerMethodField
from .models import Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta():
        model = Journal
        fields = ["id", "diaryEntryTitle", "diaryEntryDate", "diaryEntryMessage", "user_id"]


    def validate(self, attrs):
        super().validate(attrs)
        if(attrs["diaryEntryDate"] > datetime.today()):
           raise exceptions.ValidationError("date time cannot be something in the future.")

        return attrs