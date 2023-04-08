from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = [
            "category",
            "amount",
            "date",
        ]


class CreateTransactionSerializer(serializers.ModelSerializer):

    category = serializers.ChoiceField(
        choices=Track.categories,
    )

    class Meta:
        model = Track
        fields = [
            "category",
            "amount",
        ]

    def validate(self, attrs):
        attrs["user"] = self.context["request"].user

        return attrs
