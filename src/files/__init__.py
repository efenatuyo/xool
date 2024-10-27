import os
from PIL import Image
import imagehash

def remove_png():
    for root, dirs, files in os.walk("src/assets"):
        if 'template' in root:
            continue

        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(root, file)
                
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
                    
def is_similar(new_image_path, folder_path, threshold=1):
    folder_path = {"classicshirts": "src/assets/shirts", "classicpants": "src/assets/pants"}[folder_path]
    new_image_hash = imagehash.phash(Image.open(new_image_path))
    new_image_name = os.path.basename(new_image_path)
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if filename == new_image_name:
            continue
        if os.path.isfile(image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            folder_image_hash = imagehash.phash(Image.open(image_path))
            if new_image_hash - folder_image_hash < threshold:
                print(f"{new_image_name} duped by {filename}")
                return True
    return False
