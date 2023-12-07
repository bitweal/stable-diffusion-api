from django.urls import path
from .views import ImageRequestView, StatusView

urlpatterns = [
    path('', ImageRequestView.as_view(), name='image-request'),
    path('status/', StatusView.as_view(), name='status'),
]
