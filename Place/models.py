from django.db import models

# Create your models here.


class PlaceType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    highlights = models.CharField(max_length=1200, null=True, blank=True)
    bestTime = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(PlaceType, on_delete=models.CASCADE)


class PlaceImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="places/")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
