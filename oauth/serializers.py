import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


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


class BookStoreAuthSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=100)

    def validate(self, attrs):
        url = "http://booksoreapi-env.eba-3igtf73b.us-east-1.elasticbeanstalk.com/oauth/token/"
        token_response = requests.post(url=url, data={
            'code': attrs["code"],
            'client_id': settings.BOOK_STORE_CLIENT_ID,
            'client_secret': settings.BOOK_STORE_CLIENT_SECRET,
            'code_verifier': settings.BOOK_STORE_CODE_VERIFIER,
            'redirect_uri': settings.BOOK_STORE_REDIRECT_URL,
            'grant_type': 'authorization_code'
        })

        if token_response.status_code != 200:
            # Return an error response if token exchange fails
            raise serializers.ValidationError(
                f'Failed to exchange authorization code for token')

        attrs["token_res"] = token_response

        return attrs


class WalletAuthSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=100)

    def validate(self, attrs):
        url = "http://wallet-env.eba-gr5bgv3s.eu-north-1.elasticbeanstalk.com/oauth/token/"
        token_response = requests.post(url=url, data={
            'code': attrs["code"],
            'client_id': settings.WALLET_CLIENT_ID,
            'client_secret': settings.WALLET_CLIENT_SECRET,
            'code_verifier': settings.WALLET_CODE_VERIFIER,
            'redirect_uri': settings.WALLET_REDIRECT_URL,
            'grant_type': 'authorization_code'
        })

        if token_response.status_code != 200:
            # Return an error response if token exchange fails
            raise serializers.ValidationError(
                f'Failed to exchange authorization code for token')

        attrs["token_res"] = token_response

        return attrs
