from django.urls import path

from oauth2_provider.views import AuthorizationView, TokenView

from . import views

urlpatterns = [
    path("add-transaction/", views.AddTransaction.as_view(),
         name="oauth-add-transaction"),
    path("authorize/", AuthorizationView.as_view(), name="oauth-authoize"),
    path("token/", TokenView.as_view(), name="token"),
    path("login/", views.LoginOauthView.as_view(), name="oauth-login"),
    path("wallet-auth/", views.WalletAuthView.as_view(), name="bookstore-auth"),
    path("google-auth/", views.GoogleAuthView.as_view(), name="google-auth")
]
