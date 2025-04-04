import requests, random, os
import opennsfw2 as n2

from PIL import Image

def get_asset_id(cookie, clothing_id):
    try:
        response = requests.get(f'https://assetdelivery.roblox.com/v1/assetId/{clothing_id}', cookies={".ROBLOSECURITY": cookie.cookie})
        response.raise_for_status() 
        data = response.json()
        if data.get("IsCopyrightProtected"):
            print(f"Copyright Protected! ID: {clothing_id}")
            return None
        location = data.get('location')
        if location:
            asset_id_response = requests.get(location)
            asset_id_response.raise_for_status()
            asset_id_content = str(asset_id_response.content)
            asset_id = asset_id_content.split('<url>http://www.roblox.com/asset/?id=')[1].split('</url>')[0]
            return asset_id
        else:
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def get_png_url(cookie, asset_id):
    try:
        response = requests.get(f'https://assetdelivery.roblox.com/v1/assetId/{asset_id}', cookies={".ROBLOSECURITY": cookie.cookie})
        response.raise_for_status()
        data = response.json()
        if data.get("IsCopyrightProtected"):
            print(f"Copyright Protected! ID: {asset_id}")
            return None
        png_url = data.get('location')
        return requests.get(png_url).content
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def replace_template(path):
    img1 = Image.open(path)
    img2 = Image.open("src/assets/template/template.png")
    img1.paste(img2, (0,0), mask = img2)
    img1.save(path.replace("temp", ""))
    os.remove(path)

def save_asset(cookie, clothing_id, asset_type, asset_name, max_score, path_2):
 try:
    path = f"{path_2}/src/assets/temp/{asset_type}/{asset_name}_{random.randint(0, 100)}.png"
    with open(path, "wb") as f:
        f.write(get_thumbnail(clothing_id))
    if n2.predict_image(path) > max_score:
        os.remove(path)
        print("asset failed to pass nudity check")
        print(clothing_id)
        return False
    os.remove(path)
    asset_id = get_asset_id(cookie, clothing_id)
    if not asset_id:
        print("Failled to scrape asset item id")
        return False
    png = get_png_url(cookie, asset_id)
    if not png:
        print("Failed to download asset png")
        return False
    path = f"{path_2}/src/assets/temp/{asset_type}/{asset_name}_{random.randint(0, 100)}.png"
    with open(path, 'wb') as f:
        f.write(png)
    replace_template(path)
    print("downloaded one asset")
    return path.replace("temp", "")
 except Exception as e:
    print(f"ERROR: {e}")
    try:
        os.remove(path)
    except:
        pass
    return False

def get_thumbnail(asset_id):
    return requests.get(requests.post("https://thumbnails.roblox.com/v1/batch", json=[{"format": "png", "requestId": f"{asset_id}::Asset:420x420:png:regular", "size": "420x420", "targetId": asset_id, "token": "", "type": "Asset"}]).json()["data"][0]["imageUrl"]).content
