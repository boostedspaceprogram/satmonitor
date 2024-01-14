from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from GUI.Ribbon.Icons import get_icon

from Functions.Settings import Settings

import eel, threading

import os, random

class UpcomingLaunchesWindow():
    
    def __init__(self, console, parent):
        self.console = console
        self.mdiArea = parent
        self.settings = Settings(self.console)
        threading.Thread(target=self.startUI).start()
        self.show()
        
    @eel.expose
    def pick_file(folder):
        if os.path.isdir(folder):
            return random.choice(os.listdir(folder))
        else:
            return 'Not valid folder'
        
    def startUI(self):
        eel.init('src/web')
        eel.start('main.html', mode=None, port=8080)
        
    def show(self):
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowIcon(get_icon("logo_dark"))
        self.subWindow.setWindowTitle("Upcoming Launches")
        
        # Load html page
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl("http://localhost:8080/main.html"))
        self.subWindow.setWidget(self.web_view)
        
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        return self.subWindow.show()
