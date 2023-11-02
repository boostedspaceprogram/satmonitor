from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.Ribbon.Icons import get_icon

from Functions.Settings import Settings
from Functions.Livestream import Livestream

class LivestreamWindow():
    
    def __init__(self, console, parent):
        self.console = console
        self.mdiArea = parent
        self.settings = Settings(self.console)
        self.show()
        
    def show(self):
        # Livestream embed
        self.liveStream = Livestream(self.console, "https://www.youtube.com/embed/ouWMt0bBLMY?si=HO5whaFmXYgRxbp8")
        self.liveStream = self.liveStream.LivestreamView()
        
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowIcon(get_icon("logo_dark"))
        self.subWindow.setWindowTitle("Live Stream")
        self.subWindow.setWidget(self.liveStream)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        return self.subWindow.show()