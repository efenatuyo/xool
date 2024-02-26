import requests, json, time
from requests_toolbelt.multipart.encoder import MultipartEncoder

def create_asset(name, path, asset_type, cookie, group_id, description, _total_tries, wait_time):
    payload = {
        "assetType": asset_type,
        "creationContext": {
            "creator": {
                "groupId": group_id
            },
            "expectedPrice": 10
        },  
        "description": description,
        "displayName": name,
    }
    multipart_data = MultipartEncoder(
        fields={
            'request': json.dumps(payload),
            'fileContent': ('test.png', open(f'{path}', 'rb'), 'image/png')
        }
    )
    headers = {'X-CSRF-TOKEN': cookie.x_token()}
    headers['Content-Type'] = multipart_data.content_type
    dd = requests.post("https://apis.roblox.com/assets/user-auth/v1/assets", data=multipart_data, headers=headers, cookies={".ROBLOSECURITY": cookie.cookie}).json()
    if dd.get("message") == "InsufficientFunds. 10 Robux is needed.":
        print(dd["message"])
        return False
    total_tries = 0
    while total_tries < _total_tries:
        data = requests.get(f"https://apis.roblox.com/assets/user-auth/v1/operations/{dd['operationId']}", headers={'X-CSRF-TOKEN': cookie.x_token()}, cookies={".ROBLOSECURITY": cookie.cookie})
        if data.status_code == 200 and data.json().get("done") not in [None, False]:
            return data.json()
        else:
            total_tries += 1
            time.sleep(wait_time)

def release_asset(cookie, asset_id, price):
    headers = {
        "X-CSRF-TOKEN": cookie.x_token(),
        "Content-Type": "application/json",
        "Cookie": f".ROBLOSECURITY={cookie.cookie};"
    }
    data = {
        "saleAvailabilityLocation": [0, 1],
        "priceConfiguration":
            {"priceInRobux": price},
        "saleStatus": "OnSale"
    }
    return requests.post(f"https://itemconfiguration.roblox.com/v1/assets/{asset_id}/release", headers=headers, json=data)
    