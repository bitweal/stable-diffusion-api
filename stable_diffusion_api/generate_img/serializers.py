from rest_framework import serializers
from .models import ImageRequest


class ImageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRequest
        fields = '__all__'
        