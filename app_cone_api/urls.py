from django.urls import path
from .views import ConeApiView

urlpatterns = [
    path('cone/', ConeApiView.as_view(), name="cone"),
]
