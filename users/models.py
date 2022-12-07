from django.db import models

from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    is_seller = models.BooleanField(default=False)
    

    REQUIRED_FIELDS = ['first_name','last_name']