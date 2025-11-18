from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User


def notifyAdmin(heading, message, data):
    data = {
        "title": heading,
        "message": message,
        "data": data
    }

    async_to_sync(get_channel_layer().group_send)(
        "adminNotificationUpdate",
        {
            "type": "notify",
            "data": data
        }
    )


def sendData(updateData):
    async_to_sync(get_channel_layer().group_send)(
        "adminDataUpdate",
        {
            "type": "notify",
            "message": updateData
        }
    )


def notifyUser(user, title, message, data):
    group_name = ""
    if isinstance(user, User):
        if user.is_superuser:
            group_name = "adminNotificationUpdate"
        else:
            group_name = f"{user.username}-{user.id}"

        if isinstance(user, User):
            async_to_sync(get_channel_layer.group_send)(
                group_name,
                {
                    "type": "notify",
                    "data": {
                        "title": title,
                        "message": message,
                        "data": data
                    }
                }
            )