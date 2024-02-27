import src, time, json, os, random, logging, tensorflow

tensorflow.get_logger().setLevel(logging.FATAL)

class xool:
    current_directory = os.getcwd()
    types = ["classicshirts", "classicpants"]
    def __init__(self, config):
        self.config = config
        for group in config["groups"]:
            for cookie in config["groups"][group]["uploader_cookies"]:
                self.upload(cookie, group)

    def upload(self, cookie, group_id):
     cookie = src.cookie.cookie(cookie)
     while True:
      try:
        current_type = random.choice(self.types)
        items = src.scrape.scrape_assets(cookie, self.config["searching_tags"], current_type)
        random.shuffle(items)
        scraped = src.scrape.sort_assets(cookie, items[:5], self.config["blacklisted_creators"], self.config["blacklisted_words"], self.config["upload_without_blacklisted_words"]
        )
        for item in scraped:
            path = src.download.save_asset(item["id"], "shirts" if current_type == "classicshirts" else "pants", item["name"], self.config["max_nudity_value"], self.current_directory)
            if not path: continue
            item_uploaded = src.upload.create_asset(item["name"], path, "shirt" if current_type == "classicshirts" else "pants", cookie, group_id, self.config["description"], 5, 5)
            if item_uploaded is False:
                return
            src.upload.release_asset(cookie, item_uploaded['response']['assetId'], self.config["assets_price"]).json()
            print(f"Released item. ID {item_uploaded['response']['assetId']}")
            time.sleep(self.config["sleep_each_upload"])
      except:
          continue
        

xool(json.loads(open("config.json", "r").read()))
