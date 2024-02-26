import requests

def scrape_assets(cookie, keywords, subcategory):
    items =  requests.get(f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keywords}&limit=120&salesTypeFilter=1&subcategory={subcategory}", 
                        cookies={".ROBLOSECURITY": cookie.cookie}, 
                        headers={"x-csrf-token": cookie.x_token()}).json()["data"]
    return [item['id'] for item in items]

def sort_assets(cookie, ids, blacklisted_creators, blacklisted_words, upload_without_blacklisted_words):
    response = requests.post("https://catalog.roblox.com/v1/catalog/items/details", 
                            json={"items": [{"itemType": "Asset", "id": id} for id in ids]},
                            cookies={".ROBLOSECURITY": cookie.cookie},
                            headers={"x-csrf-token": cookie.x_token()}).json()["data"]
    items = []
    for item in response:
        dnd = False
        if item["creatorTargetId"] in blacklisted_creators:
            continue
        for blacklisted_word in blacklisted_words:
            if blacklisted_word in item["name"]:
                if upload_without_blacklisted_words:
                    item["name"].replace(blacklisted_word, "")
                    items.append(item)
                else:
                    dnd = True
                    break
        if dnd:
            continue
        else:
            items.append(item)
    return items
