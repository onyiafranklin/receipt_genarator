from rest_framework import generics

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope


class OauthLoginView(generics.GenericAPIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]


class AddTransaction(generics.CreateAPIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['add-transaction']
