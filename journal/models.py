from django.db import models
from users.models import User

# Create your models here.

class Journal(models.Model):
    diaryEntryTitle = models.CharField(max_length=100)
    diaryEntryDate = models.DateTimeField()
    diaryEntryMessage = models.CharField(max_length=2000)
    user_id = models.ForeignKey(to = User, related_name="journals", on_delete=models.CASCADE)

