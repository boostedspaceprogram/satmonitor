import requests

class TelegramNotificationProvider():
    
    def __init__(self, config):
        self.config = config
        self.payload = {}
        
    def send_notification(self, message):
        self.payload = {
            "chat_id": self.config["chat_id"],
            "text": message
        }
        url = "https://api.telegram.org/bot{}/sendMessage".format(self.config["bot_token"])
        requests.post(url, data=self.payload).json()
        
        
        