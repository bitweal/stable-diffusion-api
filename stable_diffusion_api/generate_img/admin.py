from django.contrib import admin
from .models import ImageRequest, InterfaceQueue, ModelVersions


@admin.register(ImageRequest)
class ImageRequestAdmin(admin.ModelAdmin):
    list_display = ('model_name',
                    'type_generate',
                    'prompt', 
                    'negative_prompt', 
                    'width', 
                    'height', 
                    'status', 
                    'path_to_img', 
                    'path_to_mask',
                    'inpainting_mask_invert',
                    'denoising_strength', 
                    'ip_address', 
                    'image_data', 
                    'errors')
    

@admin.register(InterfaceQueue)
class InterfaceQueueAdmin(admin.ModelAdmin):
    list_display = ('interface', 'status_is_busy')
   
    
@admin.register(ModelVersions)
class ModelVersionsAdmin(admin.ModelAdmin):
    list_display = ('model_name','model_full_name')