from rest_framework import views
from rest_framework.response import Response
from .models import ImageRequest, Statistics
from .generate_image import put_in_queue
from datetime import datetime


class Text2ImageView(views.APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        negative_prompt = request.data.get('negative_prompt')
        width = request.data.get('width')
        height = request.data.get('height')
        ip_address = request.data.get('ip_address')
        #ip_address = request.META.get('REMOTE_ADDR')
        
        model_name = 'mj_v1'
        type_generate = 'txt2img'
        existing_request = ImageRequest.objects.filter(ip_address=ip_address, status__in=['queued', 'processing', 'completed', 'ready', 'failed']).first()   
        
        if existing_request:
            if existing_request.status == 'ready':
                    existing_request.model_name = model_name    
                    existing_request.type_generate = type_generate    
                    existing_request.prompt = prompt
                    existing_request.negative_prompt = negative_prompt
                    existing_request.width = width
                    existing_request.height = height
                    existing_request.status = 'queued'
                    existing_request.save()
                    put_in_queue(ip_address)                          
            else:
                return Response({'status': f'{existing_request.status}'})
        else:
            image_request = ImageRequest.objects.create(
            model_name = model_name,
            type_generate = type_generate,
            prompt = prompt, 
            negative_prompt = negative_prompt,
            width = width, 
            height = height,
            status = 'queued',
            ip_address = ip_address,
            )
            put_in_queue(ip_address)    
            
        month = datetime.now().strftime("%Y-%m")
        statistics, _ = Statistics.objects.get_or_create(month=month)
        statistics.month_requests += 1
        statistics.save()
        
        return Response({'status': 'queued'})
        

class Image2ImageView(views.APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        negative_prompt = request.data.get('negative_prompt')
        width = request.data.get('width')
        height = request.data.get('height')
        path_to_img = request.data.get('path_to_img')
        path_to_mask = request.data.get('path_to_mask')
        inpainting_mask_invert = request.data.get('inpainting_mask_invert')
        denoising_strength = request.data.get('denoising_strength')
        ip_address = request.data.get('ip_address')
        #ip_address = request.META.get('REMOTE_ADDR')
        
        model_name = 'inpainting'
        type_generate = 'img2img'
        existing_request = ImageRequest.objects.filter(ip_address=ip_address, status__in=['queued', 'processing', 'completed', 'ready', 'failed']).first()      
        if existing_request:
            if existing_request.status == 'ready':
                    existing_request.model_name = model_name    
                    existing_request.type_generate = type_generate    
                    existing_request.prompt = prompt
                    existing_request.negative_prompt = negative_prompt
                    existing_request.width = width
                    existing_request.height = height
                    existing_request.status = 'queued'
                    existing_request.path_to_img = path_to_img
                    existing_request.path_to_mask = path_to_mask
                    existing_request.inpainting_mask_invert = inpainting_mask_invert
                    existing_request.denoising_strength = denoising_strength
                    existing_request.save()
                    put_in_queue(ip_address)               
            else:
                return Response({'status': f'{existing_request.status}'})
        else:
            image_request = ImageRequest.objects.create(
            model_name = model_name,
            type_generate = type_generate,
            prompt = prompt, 
            negative_prompt = negative_prompt,
            width = width, 
            height = height,
            status = 'queued',
            path_to_img = path_to_img,
            path_to_mask = path_to_mask,
            inpainting_mask_invert = inpainting_mask_invert,
            denoising_strength = denoising_strength,
            ip_address = ip_address,
            )
            put_in_queue(ip_address)       
            
        month = datetime.now().strftime("%Y-%m")
        statistics, _ = Statistics.objects.get_or_create(month=month)
        statistics.month_requests += 1
        statistics.save()

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
            