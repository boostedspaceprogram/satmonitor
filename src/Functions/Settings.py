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
            "version": "0.5.0-beta",
        }
        self.saveSettingsFile(jsonSettings)
        
    def loadSettingsFile(self):
        # Load settings.json file
        with open("settings.json", "r") as f:
            return json.load(f)
    
    def saveSettingsFile(self, jsonSettings): 
        # open file in write mode and write json
        self.console.log(f"{__class__.__name__} file saved", "debug")
        pretty_json = json.dumps(jsonSettings, indent=4, sort_keys=True)
        with open("settings.json", "w") as f:
            f.write(pretty_json)
            
    def get_settings_full(self):
        return self.loadSettingsFile()
    
    def get_settings(self, key):
        jsonSettings = self.get_settings_full()
        if jsonSettings is not None and key in jsonSettings:
            return jsonSettings[key]
        else:
            return {}
    
    def set_settings(self, key, value):
        jsonSettings = self.get_settings_full()
        if jsonSettings is not None:
            if value == "":
                jsonSettings[key] = {}
            else:
                jsonSettings[key] = value
            self.saveSettingsFile(jsonSettings)
            
    def get(self, key):
        return self.get_settings(key)
    
    def set(self, key, value):
        return self.set_settings(key, value)
            