from Notifications.TelegramNotificationProvider import TelegramNotificationProvider
from Notifications.NtfyNotificationProvider import NtfyNotificationProvider
from Notifications.DiscordNotificationProvider import DiscordNotificationProvider
from Functions.Settings import Settings

class UserNotificationProvider():
    
    # Console & Settings 
    console = None
    settings = None
    
    # Class variables
    config = {}
    
    # List of providers
    providerList = []
    
    def __init__(self, console):
        self.config = Settings(console).get_settings("notifications") or {}
        self.console = console
        self.parseConfig()
        
    def parseConfig(self):
        self.providerList = []
        
        # Loop through settings notifications file and add providers to list if enabled
        for provider in self.config:
            if self.config[provider]["enabled"]:
                self.providerList.append(provider)
            
    def send_notification(self, provider, message):
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
        
        # Log message
        if len(self.providerList) != 0:
            self.logToConsole(provider, message)
          
    def logToConsole(self, provider, message):
        self.console.log(f"{__class__.__name__} Notification sent to service: {provider.upper()} <br/> {message}", "debug")