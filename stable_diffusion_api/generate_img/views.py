from rest_framework import views
from rest_framework.response import Response
from .models import ImageRequest
from .generate_image import put_in_queue


class ImageRequestView(views.APIView):
    def post(self, request, *args, **kwargs):
        type_generate = request.data.get('type_generate')
        prompt = request.data.get('prompt')
        width = request.data.get('width')
        height = request.data.get('height')
        path_to_img = request.data.get('path_to_img')
        denoising_strength = request.data.get('denoising_strength')
        ip_address = request.data.get('ip_address')
        #ip_address = request.META.get('REMOTE_ADDR')
        
        existing_request = ImageRequest.objects.filter(ip_address=ip_address, status__in=['queued', 'processing', 'completed', 'ready', 'failed']).first()      
        if existing_request:
            if existing_request.status == 'ready':
                    existing_request.type_generate=type_generate    
                    existing_request.prompt = prompt
                    existing_request.width = width
                    existing_request.height = height
                    existing_request.status = 'queued'
                    existing_request.path_to_img = path_to_img
                    existing_request.denoising_strength = denoising_strength
                    existing_request.save()
                    put_in_queue(ip_address)               
                    return Response({'status': 'queued'})
            else:
                return Response({'status': f'{existing_request.status}'})
        else:
            image_request = ImageRequest.objects.create(
            type_generate=type_generate,
            prompt=prompt, 
            width=width, 
            height=height,
            status='queued',
            path_to_img=path_to_img,
            denoising_strength=denoising_strength,
            ip_address=ip_address,
            )
            put_in_queue(ip_address)         
            return Response({'status': 'queued'})
       

class StatusView(views.APIView):
    def post(self, request, *args, **kwargs):
        ip_address = request.data.get('ip_address')
        #ip_address = request.META.get('REMOTE_ADDR')

        existing_request = ImageRequest.objects.filter(ip_address=ip_address, status__in=['queued', 'processing', 'completed', 'ready', 'failed']).first()

        if existing_request:
            if existing_request.status == 'queued':               
                return Response({'status': 'queued'})
            
            elif existing_request.status == 'processing':
                return Response({'status': 'processing'})
            
            elif existing_request.status == 'completed':
                response_data = {'status': 'completed', 'image_data': existing_request.image_data}
                existing_request.image_data = ''
                existing_request.status = 'ready'
                existing_request.save()              
                return Response(response_data)
            
            elif existing_request.status == 'failed':
                response_data = {'status': 'failed'}
                existing_request.status = 'ready'
                existing_request.save()
                return Response(response_data)
            else:
                return Response({'status': f'{existing_request.status}'})
                
        else:
            return Response({'status': 'failed'})
            