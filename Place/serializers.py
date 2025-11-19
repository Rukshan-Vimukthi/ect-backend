from rest_framework import serializers
from .models import *

from django.conf import settings


class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        imageURL = None
        if instance.image:
            imageURL = instance.image.url

        return {
            "id": data["id"],
            "url": imageURL,
        }


class PlaceSerializer(serializers.ModelSerializer):
    placeimage_set = PlaceImageSerializer(read_only=True, many=True)
    class Meta:
        model = Place
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "id": data["id"],
            "name": data["name"],
            "about": data["about"],
            "highlights": data["highlights"],
            "bestTime": data["bestTime"],
            "location": data["location"],
            "source": data["source"],
            "images": data["placeimage_set"]
        }
