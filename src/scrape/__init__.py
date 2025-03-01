import requests, random, re

def scrape_assets(cookie, keywords, subcategory):
    
    items =  requests.get(f"https://catalog.roblox.com/v1/search/items?category=Clothing&limit=120&salesTypeFilter=1&sortAggregation={random.choice(['1', '3', '5'])}&sortType={random.randint(0, 2)}&subcategory={subcategory}&minPrice=5&keyword={keywords}", 
                        cookies={".ROBLOSECURITY": cookie.cookie}, 
                        headers={"x-csrf-token": cookie.x_token()})
    if items.status_code == 200:
        return [item['id'] for item in items.json()["data"]]
    else:
        return []

def sort_assets(cookie, ids, blacklisted_creators, blacklisted_words, upload_without_blacklisted_words):
    response = requests.post("https://catalog.roblox.com/v1/catalog/items/details", 
                            json={"items": [{"itemType": "Asset", "id": id} for id in ids]},
                            cookies={".ROBLOSECURITY": cookie.cookie},
                            headers={"x-csrf-token": cookie.x_token()})
    if response.status_code == 200:
     items = []
     for item in response.json()["data"]:
        dnd = False
        if item["creatorTargetId"] in blacklisted_creators:
            continue
        item["name"] = re.sub(r'[<>:"/\\|?*]', '_', item['name'])
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
            item["name"] = item['name'].replace("/", " ")
            items.append(item)
     return items
    elif response.status_code == 403:
        raise Exception("403")
    elif response.status_code == 429:
        raise Exception("Ratelimit hit. This may take a while to go away.")
    else:
        return []
