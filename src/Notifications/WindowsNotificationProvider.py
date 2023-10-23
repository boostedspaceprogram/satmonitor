from win11toast import notify

class WindowsNotificationProvider():
    
    def __init__(self, config):
        self.config = config
        self.payload = {}
        
    def send_notification(self, message): 
        notifyButtons = [
            {'activationType': 'protocol', 'arguments': '', 'content': 'Open'},
            {'activationType': 'protocol', 'arguments': '', 'content': 'Close'}
        ]
        
        notify(title="Sat Monitor",
            body=message,
            buttons=notifyButtons,
        )