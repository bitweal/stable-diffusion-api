from django.urls import path
from .views import Text2ImageView, Image2ImageView, StatusView


urlpatterns = [
    path('txt2img', Text2ImageView.as_view(), name='txt2img'),
    path('img2img', Image2ImageView.as_view(), name='img2img'),
    path('status', StatusView.as_view(), name='status'),
]
