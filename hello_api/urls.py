from django.urls import path
from hello_api.views import HelloView

urlpatterns = [
    path('', HelloView.as_view(), name='hello'),
]