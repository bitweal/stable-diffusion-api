from .models import ImageRequest, PortQueue
from background_task import background
import requests
from PIL import Image
from io import BytesIO
import base64


def pil_to_base64(img):
    pil_image = Image.open(img)
    with BytesIO() as stream:
        pil_image.save(stream, format="png")
        base64_str = base64.b64encode(stream.getvalue()).decode("utf-8")
        return ["data:image/png;base64," + base64_str]
    

def generate_image(ip_address: str, type_generate: str, data):  
    try:
        image_request = ImageRequest.objects.get(ip_address=ip_address, status='processing')
    except ImageRequest.DoesNotExist:
        image_request.status = 'failed'        
        image_request.erorrs = f'ImageRequest DoesNotExist'
        image_request.save()
        return   
    try:     
        port = PortQueue.objects.filter(status_is_busy=False).first()
    except PortQueue.DoesNotExist:
        image_request.status = 'failed'
        image_request.errors = 'No such port'
        image_request.save()  
        return
    port.status_is_busy = True
    port.save()
      
    url = f'http://127.0.0.1:786{port.port_number}/sdapi/v1/{type_generate}'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    } 
     
    try:      
        response = requests.post(url, headers=headers, json=data)
        status = response.status_code     
        
        if status == 200:
            image_request.status = 'completed'
            image_request.image_data = response.json()['images']
        else:
            image_request.status = 'failed'  
            image_request.erorrs = response.json()                
    except Exception as e:
        image_request.status = 'failed'        
        image_request.erorrs = f'Error: {str(e)}'
        image_request.save()
    finally:
        port.status_is_busy = False   
        port.save()
        image_request.save()   
      
        
@background(schedule=0)
def put_in_queue(ip_address):
    try:
        image_request = ImageRequest.objects.get(ip_address=ip_address, status='queued')
        type_generate = image_request.type_generate
        prompt = image_request.prompt
        width = image_request.width
        height = image_request.height
        path_to_img = image_request.path_to_img
        denoising_strength = image_request.denoising_strength
        
    except ImageRequest.DoesNotExist:
        image_request.status = 'failed'        
        image_request.erorrs = f'ImageRequest DoesNotExist'
        image_request.save()
        return
    
    image_request.status = 'processing'
    image_request.save()
    negative_prompt = "[deformed | disfigured], poorly drawn, [bad : wrong] anatomy, [extra | missing |\
            floating | disconnected] limb, (mutated hands and fingers), blurry"      
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
            "send_images": True,
            "save_images": True,
            }
            generate_image(ip_address, type_generate, data_txt2img)       
        elif type_generate == 'img2img':
            data_img2img = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "init_images": pil_to_base64(path_to_img),
            "include_init_images": True,
            "seed": -1,
            "sampler_name": "DPM++ 2M Karras",
            "denoising_strength": denoising_strength,
            "batch_size": 1,
            "steps": 50,
            "cfg_scale": 7,
            "width": width,
            "height": height,
            "restore_faces": False,
            "send_images": True,
            "save_images": True,
            }
            generate_image(ip_address, type_generate, data_img2img)
    except Exception as e:
        image_request.status = 'failed'        
        image_request.erorrs = f'Error: {e}'
        image_request.save()
        return