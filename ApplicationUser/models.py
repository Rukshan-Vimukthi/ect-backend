from django.db import models
from django.contrib.auth.models import User

from Common.models import AvailableLanguage, Currency, AgeCategory, TransportType, TourType, HotelCategory, Hotel, RoomType
from Place.models import Place

# Create your models here.
class Tourist(models.Model):
    phone = models.CharField(max_length=12)
    profile_image = models.FileField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UnregisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=100)


class TourInquiry(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    arrival = models.DateTimeField(null=True, blank=True)
    departure = models.DateTimeField(null=True, blank=True)
    arrival_airport = models.CharField(max_length=50, null=True, blank=True)
    departure_airport = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=100)
    duration_of_stay = models.IntegerField(default=1)
    need_visa_assistance = models.BooleanField(default=False)
    need_travel_insurance = models.BooleanField(default=False)
    guide_language = models.ForeignKey(AvailableLanguage, on_delete=models.CASCADE)
    transport_type = models.ManyToManyField(to=TransportType, through="TourInquiryHasTransportType")
    age_categories = models.ManyToManyField(to=AgeCategory, through="TourInquiryHasAgeCategory")
    places = models.ManyToManyField(to=Place, through="TourInquiryHasPlace")
    placesString = models.TextField(null=True, blank=True)
    estimated_budget = models.FloatField(default=0.0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    hotels = models.ManyToManyField(to=Hotel, through="TourInquiryHasHotels")
    roomType = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True)
    extraNotes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class TourPackage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.ForeignKey(TourType, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    total_price = models.FloatField()
    inclusions = models.TextField(null=True, blank=True)
    exclusions = models.TextField(null=True, blank=True)
    special_notes = models.TextField(null=True, blank=True)
    tourInquiry = models.ForeignKey(TourInquiry, on_delete=models.CASCADE, null=True, blank=True)
    package_highlights = models.TextField(null=True, blank=True)
    age_categories = models.ManyToManyField(to=AgeCategory, through="TourPackageHasAgeCategory")
    transport_type = models.ManyToManyField(to=TransportType, through="TourPackageHasTransportType")
    places = models.ManyToManyField(to=Place, through="TourPackageHasPlace")
    hotels = models.ManyToManyField(to=Hotel, through="TourPackageHasHotels")


class TourPackageHasAgeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    age_category = models.ForeignKey(AgeCategory, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    numberOfPeople = models.IntegerField(default=1)


class TourPackageHasPlace(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)


class TourPackageHasTransportType(models.Model):
    id = models.AutoField(primary_key=True)
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)


class TourPackageHasHotels(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)


class TourPackageMedia(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="packages/built-in/images")
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)


class TourInquiryHasAgeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    age_category = models.ForeignKey(AgeCategory, on_delete=models.CASCADE)
    tour_inquiry = models.ForeignKey(TourInquiry, on_delete=models.CASCADE)
    numberOfPeople = models.IntegerField(default=1)
    

class TourInquiryHasPlace(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tour_inquiry = models.ForeignKey(TourInquiry, on_delete=models.CASCADE)


class TourInquiryHasTransportType(models.Model):
    id = models.AutoField(primary_key=True)
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    tour_inquiry = models.ForeignKey(TourInquiry, on_delete=models.CASCADE)


class TourInquiryHasHotels(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tour_inquiry = models.ForeignKey(TourInquiry, on_delete=models.CASCADE)
