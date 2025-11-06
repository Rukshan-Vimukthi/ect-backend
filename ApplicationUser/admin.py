from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([TourInquiry, TourInquiryHasAgeCategory, TourInquiryHasPlace, TourPackage, UnregisteredUser])