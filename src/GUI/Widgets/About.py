from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.Ribbon.Icons import get_icon
from Functions.Settings import Settings

import requests, subprocess, sys, os, time

class AboutWindow():
    
    def __init__(self, console, parent):
        self.console = console
        self.mdiArea = parent
        self.settings = Settings(self.console)
        self.show()
    
    def show(self):
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("About - Sat Monitor")
        self.subWindow.setWindowIcon(get_icon("logo_dark"))
        self.subWindow.resize(300, 300)
        
        # qform
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)
        
        # title
        title = QLabel("Sat Monitor", form)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        form.layout().addWidget(title)
        
        # add visual line break
        line = QFrame(form)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form.layout().addWidget(line)
        
        # description
        description = QLabel("Sat Monitor is a free and open source satellite monitoring application build with Python and Qt5, it's main purpose is to provide a simple and easy to use interface to monitor satellites and other space related data.", form)
        form.layout().addWidget(description)
        
        # allow label to grow and shrink
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignTop)
        
        # version
        version = QLabel("Version: " + self.settings.get_settings("version") + "", form)
        form.layout().addWidget(version)
        
        # add visual line break
        line = QFrame(form)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form.layout().addWidget(line)

        # update button
        updateBtn = QPushButton("Check for updates", form)
        form.layout().addWidget(updateBtn)
        
        # connect update button to on_update_click function so it can be clicked and called from outside the class
        updateBtn.clicked.connect(lambda: self.on_update_click())
    
        # Set form as sub window widget
        self.subWindow.setWidget(form)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        self.subWindow.show()
        return self.subWindow
    
    def on_update_click(self):
        self.console.log("Checking for updates...", "info")
        # make request to github api and fetch latest release do not cache response
        response = requests.get("https://api.github.com/repos/boostedspaceprogram/satmonitor/releases", headers={"Cache-Control": "no-cache"})
        if response.status_code == 200:
            json = response.json()
            
            # get tag name which is a string
            tag_name = json[0]["tag_name"]
            
            # compare tag name with current version
            if tag_name != self.settings.get_settings("version"):
                self.console.log("New update found on github!", "info")
                # show message box
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowIcon(get_icon("logo_dark"))
                msgBox.setText(f"New update found on github!\nCurrent version: {self.settings.get_settings('version')}\nLatest version: {tag_name}\n\nWould you like to update now? (This will close the application)")
                msgBox.setWindowTitle("Update")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.exec_()
                
                # Check if need to update
                if msgBox.result() == QMessageBox.Ok:
                    # Download latest release
                    self.console.log("Downloading latest release...", "info")
                    # fetch latest release download url
                    downloadUrl = json[0]["assets"][0]["browser_download_url"]
                    # download latest release to temp folder
                    response = requests.get(downloadUrl, headers={"Cache-Control": "no-cache"})
                    if response.status_code == 200:
                        try:
                            # create update-temp folder if it doesn't exist
                            if not os.path.exists("update"):
                                os.makedirs("update")
                            
                            # check if other update files exist and delete them
                            for file in os.listdir("update"):
                                if file.endswith(".exe"):
                                    os.remove("update/" + file)
                            
                            # save file which is a .exe to temp folder
                            with open("update/sat-monitor-" + tag_name + ".exe", "wb") as file:
                                file.write(response.content)
                                self.console.log("Downloaded latest release and saved to update folder", "info")
                            
                            # Check if file has successfully been downloaded and saved to update folder
                            if os.path.exists("update/sat-monitor-" + tag_name + ".exe"):
                                # run latest release
                                self.console.log("Running latest release setup and closing main application", "info")
                                
                                # open new process to execute .exe file
                                command = ['cmd.exe', '/c', 'start', 'update/sat-monitor-' + tag_name + '.exe']
                                subprocess.Popen(command, shell=True)
                                
                                # close application so it can be updated
                                sys.exit()
                            else:
                                self.console.log("Error running latest release", "error")
                                # show message box
                                msgBox = QMessageBox()
                                msgBox.setIcon(QMessageBox.Information)
                                msgBox.setWindowIcon(get_icon("logo_dark"))
                                msgBox.setText(f"Error running latest release, please try again later or manually download the latest release from github")
                                msgBox.setWindowTitle("Update")
                                msgBox.setStandardButtons(QMessageBox.Ok)
                                msgBox.setDefaultButton(QMessageBox.Ok)
                                msgBox.exec_()
                        except(Exception):
                            self.console.log("Error running latest release", "error")
                            # show message box
                            msgBox = QMessageBox()
                            msgBox.setIcon(QMessageBox.Information)
                            msgBox.setWindowIcon(get_icon("logo_dark"))
                            msgBox.setText(Exception)
                            msgBox.setWindowTitle("Update")
                            msgBox.setStandardButtons(QMessageBox.Ok)
                            msgBox.setDefaultButton(QMessageBox.Ok)
                            msgBox.exec_()
                    else:
                        self.console.log("Error downloading latest release", "error")
                        # show message box
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setWindowIcon(get_icon("logo_dark"))
                        msgBox.setText(f"Error downloading latest release, please try again later or manually download the latest release from github")
                        msgBox.setWindowTitle("Update")
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        msgBox.setDefaultButton(QMessageBox.Ok)
                        msgBox.exec_()
            else:
                self.console.log("No updates found", "info")
                # show message box
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowIcon(get_icon("logo_dark"))
                msgBox.setText(f"No updates found\nCurrent version: {self.settings.get_settings('version')}")
                msgBox.setWindowTitle("Update")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.exec_()
        else:
            self.console.log("Error checking for updates", "error")
            # show message box
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(get_icon("logo_dark"))
            msgBox.setText(f"Error checking for updates")
            msgBox.setWindowTitle("Update")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec_()
            