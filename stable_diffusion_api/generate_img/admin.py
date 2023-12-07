from django.contrib import admin
from .models import ImageRequest, PortQueue

@admin.register(ImageRequest)
class ImageRequestAdmin(admin.ModelAdmin):
    list_display = ('type_generate','prompt', 'width', 'height', 'status', 'path_to_img', 'denoising_strength', 'ip_address', 'image_data', 'erorrs')
    
@admin.register(PortQueue)
class PortQueueAdmin(admin.ModelAdmin):
    list_display = ('port_number', 'status_is_busy')