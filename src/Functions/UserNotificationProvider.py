from Notifications.WindowsNotificationProvider import WindowsNotificationProvider
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
            
    def send_notification(self, message):
        # Send notification
        if "windows" in self.providerList:
            WindowsNotificationProvider(self.config["windows"]).send_notification(message)
        
        if "telegram" in self.providerList:
            TelegramNotificationProvider(self.config["telegram"]).send_notification(message)
        
        if "ntfy.sh" in self.providerList:
            NtfyNotificationProvider(self.config["ntfy.sh"]).send_notification(message)
            
        if "discord" in self.providerList:
            DiscordNotificationProvider(self.config["discord"]).send_notification(message)
        
        # Log message
        if len(self.providerList) != 0:
            self.logToConsole(message)
          
    def logToConsole(self, message):
        self.console.log(f"{__class__.__name__} Notification sent to service: {self.providerList} <br/> {message}", "debug")