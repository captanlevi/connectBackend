from django.db import models
from django.contrib.auth.models import (AbstractUser)

# Create your models here.


class User(AbstractUser):
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "dob"]

    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length= 200)
    dob = models.DateField(null = False, blank=False)

    

