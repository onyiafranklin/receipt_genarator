from django.contrib import admin
from django.urls import path, include

from .views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('transaction/', include('tracker.urls')),
    path('oauth/', include('oauth.urls')),
    path('health/', HealthCheckView.as_view(), name="health")
]
