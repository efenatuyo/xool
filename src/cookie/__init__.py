import time, requests

class cookie:
    def __init__(self, cookie):
        self.cookie = cookie
        self._x_token = None
        self.last_generated_time = 0
        self.generate_token()

    def generate_token(self):
        self._x_token = requests.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": self.cookie}).headers.get("x-csrf-token")
        self.last_generated_time = time.time()

    def x_token(self):
        current_time = time.time()
        if current_time - self.last_generated_time >= 120:
            self.generate_token()
        return self._x_token
