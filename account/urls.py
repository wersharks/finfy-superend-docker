from django.urls import path, include
from hello_api.views import HelloView

urlpatterns = [
    path('api/v1/', include('rest_registration.api.urls')),
]