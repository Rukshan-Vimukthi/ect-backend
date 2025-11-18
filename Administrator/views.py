from django.shortcuts import render

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes, api_view

from Place.models import PlaceType

# Create your views here.
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createPlaceType(request):
    response = {"status": "failed"}
    try:
        placeType = request.data["placeType"]
        placeType = PlaceType.objects.create(type=placeType)
        if placeType is not None:
            response["status"] = "ok"
    except Exception as exception:
        print(exception)

    return Response(response)
