from Notifications.TelegramNotificationProvider import TelegramNotificationProvider
from Notifications.NtfyNotificationProvider import NtfyNotificationProvider
from Notifications.DiscordNotificationProvider import DiscordNotificationProvider

from GUI.Console import Console

class UserNotificationProvider():
    
    # Console 
    console = None
    
    # Class variables
    config = {}
    
    # List of providers
    providerList = []
    
    def __init__(self, console, config):
        self.config = config
        self.console = console
        self.parseConfig()
        
    def parseConfig(self):
        for provider, _ in self.config.items():
            self.providerList.append(provider)
            
    def send_notification(self, provider, message):
        # Log message
        self.logToConsole(provider, message)
        
        # Error handling
        if provider not in self.providerList:
            self.console.log(f"{__class__.__name__} {provider} not configured", "error")
        
        # Send notification
        if "telegram" in self.providerList and provider == "telegram":
            TelegramNotificationProvider(self.config["telegram"]).send_notification(message)
        
        if "ntfy.sh" in self.providerList and provider == "ntfy.sh":
            NtfyNotificationProvider(self.config["ntfy.sh"]).send_notification(message)
            
        if "discord" in self.providerList and provider == "discord":
            DiscordNotificationProvider(self.config["discord"]).send_notification(message)
            
    def logToConsole(self, provider, message):
        self.console.log(f"{__class__.__name__} Notification sent to service: {provider.upper()} <br/> {message}", "debug")