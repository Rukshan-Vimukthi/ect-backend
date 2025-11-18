from django.shortcuts import render
from BininsNotification.models import Notification

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def markNotificationAsRead(request):
    response = {"status": "failed"}
    data = request.data
    try:
        notificationID = data["notificationID"]
        notification = Notification.objects.get(id=notificationID)
        if notification is not None:
            notification.is_read = True
            notification.save()
            response["status"] = "ok"
    except Exception as e:
        print(e)
    return Response(response)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getNotifications(request, notificationClass):
    response = {"status": "failed"}
    try:
        notifications = notificationClass.objects.all()
        response["status"] = "ok"
    except Exception as e:
        print(e)
    return Response(response)
