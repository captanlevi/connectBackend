from django.db import models
from django.contrib.auth.models import (AbstractUser)

# Create your models here.


class User(AbstractUser):
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length= 200, null = True,blank= True)
    dob = models.DateField(null = True, blank= True)