import src, time, json, os

class xool:
    current_directory = os.getcwd()
    def __init__(self, config):
        self.config = config
        for group in config["groups"]:
            for cookie in config["groups"][group]["uploader_cookies"]:
                self.upload(cookie, group)

    def upload(self, cookie, group_id):
        cookie = src.cookie.cookie(cookie)
        assert self.config["groups"][group_id]["asset_type"] in ["classicshirts", "classicpants"], f"invalid asset type. EXPECTED: ['classicshirts', 'classicpants']"
        total = self.config["groups"][group_id]["total_upload_each_account"] if self.config["groups"][group_id]["total_upload_each_account"] < 121 else 120
        scraped = src.scrape.sort_assets(cookie, 
                                    src.scrape.scrape_assets(cookie, self.config["searching_tags"], self.config["groups"][group_id]["asset_type"])
                                    [:total], self.config["blacklisted_creators"], self.config["blacklisted_words"], self.config["upload_without_blacklisted_words"]
        )
        for item in scraped:
            path = src.download.save_asset(item["id"], "shirts" if self.config["groups"][group_id]["asset_type"] == "classicshirts" else "pants", item["name"], self.config["max_nudity_value"], self.current_directory)
            if not path: continue
            item_uploaded = src.upload.create_asset(item["name"], path, "shirt" if self.config["groups"][group_id]["asset_type"] == "classicshirts" else "pants", cookie, group_id, self.config["description"], 5, 5)
            if item_uploaded is False:
                return
            print(src.upload.release_asset(cookie, item_uploaded['response']['assetId'], self.config["assets_price"]).json())
            time.sleep(self.config["sleep_each_upload"])

xool(json.loads(open("config.json", "r").read()))