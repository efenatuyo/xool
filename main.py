import src, time, json, os, random, logging, tensorflow, traceback

tensorflow.get_logger().setLevel(logging.FATAL)
    
class xool:
    current_directory = os.getcwd()
    types = ["classicshirts", "classicpants"]
    def __init__(self, config):
        src.files.remove_png()
        self.config = config
        for group in config["groups"]:
            for cookie in config["groups"][group]["uploader_cookies"]:
                self.upload(cookie, group)

    def upload(self, cookie, group_id):
     if not cookie:
         raise Exception("Empty cookie")
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
            if not path: 
                continue
            if self.config["require_one_tag_in_name"]:
                if any(value.lower() in os.path.basename(path).lower().split(" ") for value in self.config["searching_tags"].split(",")):
                    continue
            if src.files.is_similar(path, current_type):
                continue
            item_uploaded = src.upload.create_asset(item["name"], path, "shirt" if current_type == "classicshirts" else "pants", cookie, group_id, self.config["description"], 5, 5)
            if item_uploaded is False:
                return
            response = src.upload.release_asset(cookie, item_uploaded['response']['assetId'], self.config["assets_price"], item["name"], self.config["description"], group_id)
            if response.status_code == 200 and response.json()["status"] == 0:
                print(f"Released item. ID {item_uploaded['response']['assetId']}")
            else:
                print(f"Failed to release item. ID {item_uploaded['response']['assetId']}")
            time.sleep(self.config["sleep_each_upload"])
      except Exception as e:
          if str(e) == "403":
              print("403")
              continue
              raise Exception("Invalid cookie") 
          print(f"ERROR: {traceback.format_exc()}")
        

xool(json.loads(open("config.json", "r").read()))
