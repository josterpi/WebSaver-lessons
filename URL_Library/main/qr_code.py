import qrcode
import os
from django.conf import settings

def generate_qr_code(url, name, size=6, border_size=4, color1='black', color2='white'):
    # resolves directory for created image
    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_code_dir, exist_ok=True)
    # qrcode attributes
    qr = qrcode.QRCode(
        version=1,
        box_size=size,
        border=border_size
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color1, back_color=color2)
    file_name = f'{name}.png'  # FIXME filename collision if the same name is used twice
    full_path = os.path.join(qr_code_dir, file_name)
    img.save(full_path)
    
    # Return relative path (for database and URLs)
    # FIXME This gets saved in the DB which will break if settings.MEDIA_ROOT ever changes 
    return f'/media/qr_codes/{file_name}'
