import os, json, time

class Settings:
    
    console = None
    
    def __init__(self, console):
        self.console = console
        self.checkSettingsFile()
        
    def checkSettingsFile(self):
        # Check if settings.json file exist
        if not os.path.isfile("settings.json"):
            self.console.log(f"{__class__.__name__} not found", "info")
            self.createSettingsFile()
        
        self.console.log(f"{__class__.__name__} found", "info")
        return self.loadSettingsFile()
            
    def createSettingsFile(self):
        # Create settings.json file
        self.console.log(f"{__class__.__name__} file created", "debug")
        jsonSettings = {
            "created_at": time.time(),
            "theme": "default",
        }
        self.saveSettingsFile(json.dumps(jsonSettings))
        
    def loadSettingsFile(self):
        # Load settings.json file
        self.console.log(f"{__class__.__name__} file loaded", "debug")
        with open("settings.json", "r") as f:
            return json.load(f)
    
    def saveSettingsFile(self, json): 
        # open file in write mode and write json
        self.console.log(f"{__class__.__name__} file saved", "debug")
        with open("settings.json", "w") as f:
            f.write(json)
            
    def get_settings(self):
        return self.loadSettingsFile()
    
    def set_settings(self, key, value):
        jsonSettings = self.get_settings()
        jsonSettings[key] = value
        self.saveSettingsFile(json.dumps(jsonSettings))
            