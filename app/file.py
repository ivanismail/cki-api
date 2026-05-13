import os
import base64
import uuid
from datetime import datetime

IMG_DIR = "/var/www/html/cki-api/images/"
UPLOAD_DIR = "images"

os.makedirs(IMG_DIR, exist_ok=True)

def save_base64_image(base64_str: str) -> str:
    try:
        # Handle jika ada prefix data:image/png;base64,...
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        # Decode base64
        image_data = base64.b64decode(base64_str)

        # Generate nama file unik
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.jpg"
        file_path = os.path.join(IMG_DIR, filename)

        # Simpan file
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Return path relatif (untuk disimpan di DB)
        return f"{UPLOAD_DIR}/{filename}"

    except Exception as e:
        raise ValueError(f"Gagal menyimpan gambar: {str(e)}")