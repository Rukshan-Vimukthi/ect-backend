from rest_framework import serializers
from .models import ExternalContact

class ExternalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalContact
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return {
            "id": data["id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "phone": data["phone"],
            "subject": data["subject"],
            "message": data["message"]
        }