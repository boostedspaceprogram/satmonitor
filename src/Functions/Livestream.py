from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class Livestream():
    
    # Console
    console = None
    
    # Class properties
    url = None
    
    def __init__(self, console, url):
        # Log message
        self.console = console
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # Livestream type
        self.set_url(url)

    def LivestreamView(self):
        self.console.log(f"Opening livestream: {self.get_url()}", "info")
        
        # Livesstream initialization
        self.liveStream = QWebEngineView()
        self.liveStream.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False) # Allow autoplay
        self.liveStream.setHtml(f'''
        <body style="margin:0px;padding:0px;overflow:hidden">
            <iframe src="{self.get_url()}" style="overflow:hidden;height:100%;width:100%" height="100%" width="100%" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </body>
        ''')
        
        return self.liveStream
        
        
        
    # ----------------- GETTERS AND SETTERS ----------------- #
    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url