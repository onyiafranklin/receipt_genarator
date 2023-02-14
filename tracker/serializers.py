from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Track

class TrackSerializer(serializers.ModelSerializer):

    month = serializers.IntegerField(
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
            ],
            required=True,
            write_only=True
        )
        
    year = serializers.IntegerField(
        validators = [
            MaxValueValidator(datetime.now().year),
            MinValueValidator(datetime.now().year-20)
        ],
        write_only=True
        )
    
    category = serializers.ChoiceField(
        choices=Track.categories,
        read_only=True
    )
    
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["amount"].read_only = True
        self.fields["date"].read_only = True

    class Meta:
        model = Track
        fields = [
            "category",
            "amount",
            "date",
            "year",
            "month"
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



