from django.db import models

class ImageRequest(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]

    type_generate = models.TextField(max_length=10)
    prompt = models.TextField()
    negative_prompt = models.TextField(default="")
    width = models.IntegerField()
    height = models.IntegerField()   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)   
    path_to_img = models.TextField(default="")
    path_to_mask = models.TextField(default="")
    inpainting_mask_invert = models.IntegerField(default=0)
    denoising_strength = models.FloatField(default=0.5)
    ip_address = models.GenericIPAddressField()
    image_data = models.TextField(blank=True, null=True)
    erorrs = models.TextField()
    

class PortQueue(models.Model):
    port_number = models.IntegerField(unique=True)
    status_is_busy = models.BooleanField(default=False)