from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=50)
    content = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
