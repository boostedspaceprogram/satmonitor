from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *
from Functions.Globe import Globe
from Functions.Livestream import Livestream
from Functions.TLE import TLE
from Functions.Requests import Requests
from Functions.Settings import Settings

import os, sys, json, time

class MDI():
    
    console = None
    mdiArea = None
    settings = None
    
    def __init__(self, console):
        # Console class
        self.console = console
        
        # Settings class
        self.settings = Settings(self.console)
        
        # Console message
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # MDI initialization/properties
        self.mdiArea = QMdiArea()
        
        # self.Globe3D()
        
        # self.Globe2D()
        
        # self.embedLivestream()
        
        # self.TLEWindow()
        
        # self.upcomingLaunchesWindow()
        
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
       
    def TLEWindow(self):
        # TLE data class
        self.TLE = TLE(self.console, "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=json")
        self.TLE = self.TLE.TLETable()
        
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("TLE Data")
        self.subWindow.resize(600, 500)
        self.subWindow.setWidget(self.TLE)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        return self.subWindow
        
    def upcomingLaunchesWindow(self):
        self.upcomingLaunches = Requests(self.console, "https://ll.thespacedevs.com/2.2.0/launch/upcoming/")
        self.upcomingLaunches.set_method("GET")
        self.upcomingLaunches.set_headers({"User-Agent": "SatMonitor/1.0", "Accept": "application/json"})
        self.upcomingLaunchesData = self.upcomingLaunches.make_requests()
        
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Upcoming Launches")
        self.subWindow.resize(800, 300)
        
        # Create a QTreeWidget widget 
        self.treeWidget = QTreeWidget()
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setSortingEnabled(True)
        
        # Set tree widget columns
        if self.upcomingLaunchesData is not None:
            self.subWindow.setWindowTitle("Upcoming Launches - " + str(len(self.upcomingLaunchesData["results"])) + " results")
            self.treeWidget.setColumnCount(6)
            self.treeWidget.setHeaderLabels(["Rocket", "Mission", "Net", "Status", "Pad", "Location"])
        else:
            self.treeWidget.setColumnCount(1)
            self.treeWidget.setHeaderLabels(["Error"])
        
        # sort by column 2 'Net' ascending
        if self.upcomingLaunchesData is not None:
            self.treeWidget.sortByColumn(2, Qt.AscendingOrder)
        
        # fit column 'Rocket', 'Mission', 'Net' and 'Status' to full width
        if self.upcomingLaunchesData is not None:
            self.treeWidget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.treeWidget.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.treeWidget.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.treeWidget.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Add data to main tree widget
        if self.upcomingLaunchesData is not None:
            for launch in self.upcomingLaunchesData["results"]:
                mainWidgetItem = QTreeWidgetItem(self.treeWidget)
                
                # Add data to main widget item columns
                mainWidgetItem.setText(0, launch["rocket"]["configuration"]["name"])
                mainWidgetItem.setText(1, launch["mission"]["name"])
                mainWidgetItem.setText(2, launch["net"])
                mainWidgetItem.setText(3, launch["status"]["name"])
                mainWidgetItem.setText(4, launch["pad"]["name"])
                mainWidgetItem.setText(5, launch["pad"]["location"]["name"])
                
                # Add double click event to main widget item
                mainWidgetItem.setFlags(mainWidgetItem.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)     
        else:
            mainWidgetItemNoData = QTreeWidgetItem(self.treeWidget)
            mainWidgetItemNoData.setText(0, "No data available from API, please try again later.")
            
        # Add double click event on any tree widget item
        self.treeWidget.itemDoubleClicked.connect(self.on_treeWidget_itemDoubleClicked)
        
        # Set tree widget as sub window widget
        self.subWindow.setWidget(self.treeWidget)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        return self.subWindow

    def on_treeWidget_itemDoubleClicked(self, item):
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Upcoming Launches Details - " + item.text(1))
        self.subWindow.resize(400, 300)
        
        # Create a QTreeWidget widget
        self.treeWidget = QTreeWidget()
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderHidden(False)
        
        # Set tree widget columns
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Info", "Value"])
        
        # loop trough data and add to tree widget
        for launchDetails in self.upcomingLaunchesData["results"]:
            if launchDetails["rocket"]["configuration"]["name"] == item.text(0) and launchDetails["mission"]["name"] == item.text(1):
                for key, value in launchDetails.items():
                    mainWidgetItem = QTreeWidgetItem(self.treeWidget)
                    mainWidgetItem.setText(0, key)
                    mainWidgetItem.setText(1, str(value))
        
        # show sub window 
        self.subWindow.setWidget(self.treeWidget)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        self.subWindow.show()
        return self.subWindow
    
    def settingsWindow(self):
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Settings")
        self.subWindow.resize(400, 300)
        
        # create form
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        self.themeDropdown = QComboBox(form)
        layout.addRow("Theme: ", self.themeDropdown)
        
        themes = [
            'default',
            'dark_amber.xml',
            'dark_blue.xml',
            'dark_cyan.xml',
            'dark_lightgreen.xml',
            'dark_pink.xml',
            'dark_purple.xml',
            'dark_red.xml',
            'dark_teal.xml',
            'dark_yellow.xml',
            'light_amber.xml',
            'light_blue.xml',
            'light_cyan.xml',
            'light_cyan_500.xml',
            'light_lightgreen.xml',
            'light_pink.xml',
            'light_purple.xml',
            'light_red.xml',
            'light_teal.xml',
            'light_yellow.xml'
        ]
        
        # add themes to dropdown list
        for theme in themes:
            self.themeDropdown.addItem(theme)
            
        # select current theme from settings file
        self.themeDropdown.setCurrentText(self.settings.get_settings()["theme"])

        saveBtnForm = QPushButton("Save")
        saveBtnForm.clicked.connect(self.on_saveBtnForm_clicked)
        layout.addRow(saveBtnForm)
        
        # Set form as sub window widget
        self.subWindow.setWidget(form)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        self.subWindow.show()
        return self.subWindow
    
    def on_saveBtnForm_clicked(self):
        self.console.log("Settings saved", "debug")
        
        # Save settings 
        self.settings.set_settings("theme", self.themeDropdown.currentText())
        
        # Restart application to apply new theme
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)