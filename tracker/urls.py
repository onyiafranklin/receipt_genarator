from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.FetchTransactionView.as_view(), name="transactions"),
    path("add/", views.AddTransactionView.as_view(), name="add"),
]