import requests
import boto3
from botocore.exceptions import ClientError

from django.views import generic
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope

from .forms import LoginForm
from tracker.serializers import TrackSerializer
from . import serializers


User = get_user_model()


class AddTransaction(generics.CreateAPIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['add-transaction']
    serializer_class = TrackSerializer


class LoginOauthView(generic.FormView):

    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)

        login(self.request, user=user)

        return redirect(self.request.GET["next"])


class GoogleAuthView(generics.GenericAPIView):

    serializer_class = serializers.GoogleAuthSerializer

    def post(self, request):

        # Exchange the authorization code for an access token and user info
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        token_response = serializer.validated_data["token_res"]
        token_data = token_response.json()
        access_token = token_data['access_token']

        user_response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}')

        if user_response.status_code != 200:
            # Return an error response if user info retrieval fails
            return Response({'error': 'Failed to retrieve user info from Google'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_response.json()
        email = user_data.get('email')
        first_name = user_data.get('given_name')
        last_name = user_data.get('family_name')

        # Create a new user account with the user info
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(None)
            )
            client = boto3.client('sns', region_name=settings.AWS_REGION)
            try:
                response = client.subscribe(
                    TopicArn=settings.SNS_TOPIC_ARN, Protocol='email', Endpoint=user.email)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidParameter':
                    raise serializers.ValidationError(
                        {'email': 'Invalid email address'})
                elif e.response['Error']['Code'] == 'EndpointDisabled':
                    raise serializers.ValidationError(
                        {'email': 'Email address is disabled'})
                elif e.response['Error']['Code'] == 'AuthorizationError':
                    raise serializers.ValidationError(
                        f'Authorization error: {e}')
                else:
                    raise serializers.ValidationError(f'Unexpected error: {e}')
            except:
                pass

        except:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Failed to authenticate user from Google'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token)
        }

        return Response(response, status=status.HTTP_200_OK)


class BookStoreAuthView(generics.GenericAPIView):
    serializer_class = serializers.BookStoreAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        token_response = serializer.validated_data["token_res"]
        token_data = token_response.json()
        access_token = token_data['access_token']

        user_response = requests.get(
            f'http://booksoreapi-env.eba-3igtf73b.us-east-1.elasticbeanstalk.com/oauth/userinfo/',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if user_response.status_code != 200:
            # Return an error response if user info retrieval fails
            return Response({'error': 'Failed to retrieve user info from Bookstore'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_response.json()
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        # Create a new user account with the user info
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(None)
            )
            client = boto3.client('sns', region_name=settings.AWS_REGION)
            try:
                response = client.subscribe(
                    TopicArn=settings.SNS_TOPIC_ARN, Protocol='email', Endpoint=user.email)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidParameter':
                    raise serializers.ValidationError(
                        {'email': 'Invalid email address'})
                elif e.response['Error']['Code'] == 'EndpointDisabled':
                    raise serializers.ValidationError(
                        {'email': 'Email address is disabled'})
                elif e.response['Error']['Code'] == 'AuthorizationError':
                    raise serializers.ValidationError(
                        f'Authorization error: {e}')
                else:
                    raise serializers.ValidationError(f'Unexpected error: {e}')

        except:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Failed to authenticate user from BookStore'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token)
        }

        return Response(response, status=status.HTTP_200_OK)
