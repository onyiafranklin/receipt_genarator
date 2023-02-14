from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("details/", views.AccountView.as_view(), name="account-details"),
    path("register/", views.RegisterView.as_view(), name="register")
]