from .models import ImageRequest, InterfaceQueue
from background_task import background
import requests
from PIL import Image
from io import BytesIO
import base64
import time 


def pil_to_base64(img):
    pil_image = Image.open(img)
    with BytesIO() as stream:
        pil_image.save(stream, format="png")
        base64_str = base64.b64encode(stream.getvalue()).decode("utf-8")
        return "data:image/png;base64," + base64_str
    

def generate_image(ip_address: str, type_generate: str, data):  
    try:
        image_request = ImageRequest.objects.get(ip_address=ip_address, status='processing')
    except ImageRequest.DoesNotExist:
        image_request.status = 'failed'        
        image_request.erorrs = f'ImageRequest DoesNotExist'
        image_request.save()
        return   
    try:     
        interface = InterfaceQueue.objects.filter(status_is_busy=False).first()
    except InterfaceQueue.DoesNotExist:
        image_request.status = 'failed'
        image_request.errors = 'No such interface'
        image_request.save()  
        return
    interface.status_is_busy = True
    interface.save()
            
    url_set_model = f'http://{interface.interface}/sdapi/v1/options'
    
    if type_generate == 'txt2img':
        option_payload = {
        "sd_model_checkpoint": "mj_v1.safetensors [514f5cc25b]",
        "CLIP_stop_at_last_layers": 2
        }
        response = requests.post(url=url_set_model, json=option_payload)
    elif type_generate == 'img2img':
        option_payload = {
        "sd_model_checkpoint": "Deliberate_v4-inpainting.safetensors [aadce23ddd]",
        "CLIP_stop_at_last_layers": 2
        }
        response = requests.post(url=url_set_model, json=option_payload)  

    url = f'http://{interface.interface}/sdapi/v1/{type_generate}'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    } 
     
    try:      
        response = requests.post(url=url, headers=headers, json=data)
        status = response.status_code        
        
        if status == 200:
            image_request.status = 'completed'
            image_request.image_data = response.json()['images'][0]
        else:
            image_request.status = 'failed'  
            image_request.erorrs = response.json()                
    except Exception as e:
        image_request.status = 'failed'        
        image_request.erorrs = f'Error: {str(e)}'
        image_request.save()
        time.sleep(60)      
    finally:
        interface.status_is_busy = False   
        interface.save()
        image_request.save()   
      
        
@background(schedule=0)
def put_in_queue(ip_address):
    try:
        image_request = ImageRequest.objects.get(ip_address=ip_address, status='queued')
        type_generate = image_request.type_generate
        prompt = image_request.prompt
        negative_prompt = image_request.negative_prompt
        width = image_request.width
        height = image_request.height
        path_to_img = image_request.path_to_img
        path_to_mask = image_request.path_to_mask
        inpainting_mask_invert = image_request.inpainting_mask_invert
        denoising_strength = image_request.denoising_strength
        
    except ImageRequest.DoesNotExist:
        image_request = ImageRequest.objects.get(ip_address=ip_address)
        image_request.status = 'failed'        
        image_request.erorrs = f'ImageRequest DoesNotExist'
        image_request.save()
        return
    
    image_request.status = 'processing'
    image_request.save()
    
    try:
        if type_generate == 'txt2img':
            data_txt2img = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": -1,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            "steps": 30,
            "cfg_scale": 7,
            "width": width,
            "height": height,
            "restore_faces": False,
            "tiling": False,
            "send_images": True,
            "save_images": True,
            "alwayson_scripts": {
                "ADetailer": {
                  "args": [
                    {
                      "ad_model": "face_yolov8s.pt"
                    }
                  ]
                }   
            }
            }
            generate_image(ip_address, type_generate, data_txt2img)       
        elif type_generate == 'img2img':
            data_img2img = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "init_images": [pil_to_base64(path_to_img)],
            "mask": pil_to_base64(path_to_mask),
            "inpainting_mask_invert": inpainting_mask_invert,
            "inpainting_fill": 1,
            "inpaint_full_res": 1,
            "inpaint_full_res_padding": 32,
            "include_init_images": True,
            "seed": -1,
            "sampler_name": "DPM++ 2M Karras",
            "denoising_strength": denoising_strength,
            "batch_size": 1,
            "steps": 40,
            "cfg_scale": 7,
            "width": width,
            "height": height,
            "restore_faces": False,
            "tiling": False,
            "send_images": True,
            "save_images": True,
            "alwayson_scripts": {
                "ADetailer": {
                  "args": [
                    {
                      "ad_model": "face_yolov8s.pt"
                    }
                  ]
                }   
            }
            }
            generate_image(ip_address, type_generate, data_img2img)
    except Exception as e:
        image_request.status = 'failed'        
        image_request.erorrs = f'Error: {e}'
        image_request.save()
        return