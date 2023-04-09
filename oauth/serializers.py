import requests

from django.conf import settings
from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=100)

    def validate(self, attrs):
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
            'code': attrs["code"],
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URL,
            'grant_type': 'authorization_code'
        })

        if token_response.status_code != 200:
            # Return an error response if token exchange fails
            raise serializers.ValidationError(
                'Failed to exchange authorization code for token')

        attrs["token_res"] = token_response

        return attrs
