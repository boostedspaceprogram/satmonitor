from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Functions.Globe import Globe
from Functions.Livestream import Livestream

class MDI():
    
    console = None
    
    def __init__(self, console):
        # Console class
        self.console = console
        
        # Console message
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # MDI initialization/properties
        self.mdiArea = QMdiArea()
        
        self.Globe3D()
        
        self.Globe2D()
        
        self.embedLivestream()
        
    def Globe3D(self):
        
        # Create 3D globe
        self.globe3d = Globe(self.console, "3D", "Cesium Globe", {
            "shouldAnimate": True,
            "homeButton": False,
            "navigationHelpButton": False,
        })
        
        # Globe sub window
        globe_3d_subwindow = QMdiSubWindow()
        globe_3d_subwindow.setWindowTitle(self.globe3d.get_window_title())
        
        # Create a QWebEngineView widget
        self.WebView3D = QWebEngineView()
        globe_3d_subwindow.setWidget(self.WebView3D)
        
        # Load the CesiumJS webpage
        self.WebView3D.setHtml(self.globe3d.html_out())
        
        self.mdiArea.addSubWindow(globe_3d_subwindow)  

    def Globe2D(self):
        
        # Create 2D globe
        self.globe2d = Globe(self.console, "2D", "Map", {
            "shouldAnimate": True,
            "homeButton": False,
            "navigationHelpButton": False,
            "sceneMode": "Cesium.SceneMode.SCENE2D",
        })
        
        # Globe sub window
        globe_2d_subwindow = QMdiSubWindow()
        globe_2d_subwindow.setWindowTitle(self.globe2d.get_window_title())
        
        # Create a QWebEngineView widget
        self.WebView2D = QWebEngineView()
        globe_2d_subwindow.setWidget(self.WebView2D)
        
        # Load the CesiumJS webpage
        self.WebView2D.setHtml(self.globe2d.html_out())
        
        self.mdiArea.addSubWindow(globe_2d_subwindow)
        
    def embedLivestream(self):
        # Livestream embed
        self.liveStream = Livestream(self.console, "https://www.youtube.com/embed/4aMf9K_ZaAI?autoplay=1&mute=1")
        self.liveStream = self.liveStream.LivestreamView()
        
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Live Stream")
        self.subWindow.setWidget(self.liveStream)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
       