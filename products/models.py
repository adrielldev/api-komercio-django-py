from django.db import models
from users.models import User
import uuid

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,default='')

