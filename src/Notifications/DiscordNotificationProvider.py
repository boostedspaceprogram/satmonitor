import requests, json

class DiscordNotificationProvider():
    
    def __init__(self, config):
        self.config = config
        
    def send_notification(self, message):
        method = "POST"
        url = self.config["webhook_url"]
        data = {
            "content": message,
            "tts": False,
            "embeds": [],
            "components": [],
            "actions": {},
            "username": "SatMonitor"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "SatMonitor/1.0"
        }
        data = json.dumps(data)
        encoded_data = data.encode("utf-8")
        requests.request(method=method, url=url, data=encoded_data, headers=headers).json()
        
        
        