from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "id": data["id"],
            "firstName": data["first_name"],
            "lastName": data["last_name"]
        }


class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tourist
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        return {
            "phone": data["phone"],
            "profile_image": data["profile_image"],
            "user": data["user"]
        }
    

class TourInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourInquiry
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    

class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
