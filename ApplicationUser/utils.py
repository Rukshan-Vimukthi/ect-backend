from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

from .serializers import TouristSerializer, TourInquirySerializer, TourPackageSerializer

from .models import Tourist, Place, TourInquiry, TourPackage
from Chat.models import ExternalContact
from Chat.serializers import ExternalContactSerializer

from Place.serializers import PlaceSerializer

@sync_to_async
def get_data():
    data = {}
    tourists = Tourist.objects.all()
    places = Place.objects.all()
    externalContacts = ExternalContact.objects.all()
    tourInquiries = TourInquiry.objects.all()
    tourPackages = TourPackage.objects.all()

    data["tourists"] = TouristSerializer(tourists, many=True).data
    data["places"] = PlaceSerializer(places, many=True).data
    data["tourPackages"] = TourPackageSerializer(tourPackages, many=True).data
    data["inquiries"] = TourInquirySerializer(tourInquiries, many=True).data
    data["externalMessages"] = ExternalContactSerializer(externalContacts, many=True).data
    return data