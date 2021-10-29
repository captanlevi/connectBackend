from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

class Journal(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default= timezone.now)
    message = models.CharField(max_length=2000)
    user_id = models.ForeignKey(to = User, related_name="journals", on_delete=models.CASCADE)

