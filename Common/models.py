from django.db import models

# Create your models here.
class TourType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)


class AgeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)


class TransportType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)


class AvailableLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=50)


class HotelCategory(models.Model):
    id = models.AutoField(primary_key=True)
    star_rating = models.FloatField(default=3.0, null=True)
    category = models.CharField(max_length=50)

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=15)


class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(HotelCategory, on_delete=models.CASCADE)


class MealPlan(models.Model):
    id = models.AutoField(primary_key=True)
    meal_plan = models.CharField(max_length=15)


class Accommodation(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_category = models.ForeignKey(HotelCategory, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=5)

