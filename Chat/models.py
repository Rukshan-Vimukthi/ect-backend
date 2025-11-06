from django.db import models
from django.contrib.auth.models import User
from ApplicationUser.models import UnregisteredUser

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    anonymous_user = models.ForeignKey(UnregisteredUser, on_delete=models.CASCADE, related_name="anonymous_user", null=True, blank=True)
    accepted = models.BooleanField(default=False)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
