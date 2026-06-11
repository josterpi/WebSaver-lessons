import qrcode
import os
from django.conf import settings

def generate_qr_code(url, name, size=6, border_size= 4, color1 = 'black', color2= 'white'): # 2 required arguments, 4 optional
    # resolves directory for created image
    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_code_dir, exist_ok=True)
    # qrcode attributes
    qr=qrcode.QRCode(
        version = 1,
        box_size = size,
        border = border_size
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color = color1, back_color= color2)  # qrcode.image.pil.PilImage
    file_name = f'{name}.png' #creates filename
    full_path = os.path.join(qr_code_dir, file_name) #creates full image path
    img.save(full_path) # saves image to file path
    
    # Return relative path (for database and URLs)
    return f'/media/qr_codes/{file_name}'