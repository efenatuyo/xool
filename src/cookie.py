import requests

def get_x_token(cookie):
    return requests.post("https://economy.roblox.com/", headers={"Cookie": f".ROBLOSECURITY={cookie};"}).headers.get("x-csrf-token")