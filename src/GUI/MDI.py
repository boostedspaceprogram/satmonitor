from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *

from Functions.Requests import Requests
from Functions.Settings import Settings
from Functions.UserNotificationProvider import UserNotificationProvider

from GUI.Widgets.About import *
from GUI.Widgets.Livestream import *
from GUI.Widgets.UpcomingLaunches import *
from GUI.Ribbon.Icons import get_icon

import os, sys, eel

class MDIArea(QMdiArea):

    def __init__(self, background_pixmap, parent = None):
        QMdiArea.__init__(self, parent)
        self.background_pixmap = background_pixmap
        self.centered = True
        self.display_pixmap = None
            
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self.viewport())
        painter.fillRect(event.rect(), QBrush(self.palette().color(QPalette.Window)))
        x = int(self.width() / 2 - self.display_pixmap.width() / 2)
        y = int(self.height() / 2 - self.display_pixmap.height() / 2) 
        painter.drawPixmap(x, y, self.display_pixmap)
        painter.end()
    
    def resizeEvent(self, event):
        windowHeight = event.size().height()
        if windowHeight >= 800:
            max_size = QSize(event.size().width() - 500, event.size().height() - 500)
        elif windowHeight >= 600:
            max_size = QSize(event.size().width() - 300, event.size().height() - 300)
        elif windowHeight >= 400:
            max_size = QSize(event.size().width() - 200, event.size().height() - 200)
        else:
            max_size = QSize(event.size().width(), event.size().height())
        self.display_pixmap = self.background_pixmap.scaled(max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
class MDI():
    
    console = None
    mdiArea = None
    widget = None
    settings = None
    userNotificationProvider = None
    
    def __init__(self, console):
        # Console class
        self.console = console
        
        # Settings class
        self.settings = Settings(self.console)
        
        # Console message
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # MDI initialization/properties
        self.mdiArea = MDIArea(QPixmap(get_icon("logo_dark").pixmap(QSize(2048, 2048))))

        # User notification provider
        self.userNotificationProvider = UserNotificationProvider(self.console)
        
        # self.LivestreamWindow()
        
        # self.upcomingLaunchesWindow()
        
    def AboutWindow(self):
        return AboutWindow(self.console, self.mdiArea)
    
    def LivestreamWindow(self):
        return LivestreamWindow(self.console, self.mdiArea)
    
    def upcomingLaunchesWindow(self):
        return UpcomingLaunchesWindow(self.console, self.mdiArea)
    
    def settingsWindow(self):
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Settings")
        self.subWindow.setWindowIcon(get_icon("logo_dark"))
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
        self.themeDropdown.setCurrentText(self.settings.get_settings('theme'))

        saveBtnForm = QPushButton("Save")
        saveBtnForm.clicked.connect(self.on_settingsFormSave_clicked)
        layout.addRow(saveBtnForm)
        
        # Set form as sub window widget
        self.subWindow.setWidget(form)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        self.subWindow.show()
        return self.subWindow
    
    def on_settingsFormSave_clicked(self):
        self.console.log("Settings saved", "debug")
        
        # Save settings 
        self.settings.set_settings("theme", self.themeDropdown.currentText())
        
        # Restart application to apply new theme
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        
    def alertWindow(self):
        
        # Create a QMdiSubWindow widget
        self.subWindow = QMdiSubWindow()
        self.subWindow.setWindowTitle("Alerts")
        self.subWindow.setWindowIcon(get_icon("logo_dark"))
        self.subWindow.resize(500, 400)
        
        # create form
        self.alertForm = QWidget()
        layout = QFormLayout(self.alertForm)
        self.alertForm.setLayout(layout)
        
        # title
        title = QLabel("Alerts", self.alertForm)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.alertForm.layout().addWidget(title)
        
        # description
        description = QLabel("If you want to receive alerts, fill the required fields below.", self.alertForm)
        self.alertForm.layout().addWidget(description)
        
        # Windows 10/11 notifications
        self.windowsGroupBox()
        
        # Telegram group box
        self.telegramGroupBox()
        
        # Discord group box
        self.discordGroupBox()
        
        # Ntfy.sh group box
        self.ntfyshGroupBox()

        # add save button down below the form
        saveBtnForm = QPushButton("Save")
        saveBtnForm.clicked.connect(self.on_alertFormSave_clicked)
        self.alertForm.layout().addWidget(saveBtnForm)
        
        # Set form as sub window widget
        self.subWindow.setWidget(self.alertForm)
        
        # Add the QMdiSubWindow widget to the QMdiArea widget
        self.mdiArea.addSubWindow(self.subWindow)
        self.subWindow.show()
        return self.subWindow
    
    def on_alertFormSave_clicked(self):
        self.console.log("Alerts saved", "debug")
        
        # Save settings
        self.settings.set_settings("notifications", {
            "windows": {
                "enabled": self.windowsBox.isChecked()
            },
            "telegram": {
                "enabled": self.telegramBox.isChecked(),
                "chat_id": self.telegramChatIdInput.text(),
                "bot_token": self.telegramTokenInput.text()
            },
            "discord": {
                "enabled": self.discordBox.isChecked(),
                "webhook_url": self.discordWebhookInput.text()
            },
            "ntfy.sh": {
                "enabled": self.ntfyBox.isChecked(),
                "webhook_url": self.ntfyWebhookInput.text()
            }
        })
        
        self.userNotificationProvider = UserNotificationProvider(self.console)
        
        # show popup QMessageBox
        self.QMessageBox = QMessageBox()
        self.QMessageBox.setWindowTitle("Alerts")
        self.QMessageBox.setText("Saved successfully")
        self.QMessageBox.setIcon(QMessageBox.Information)
        self.QMessageBox.setStandardButtons(QMessageBox.Ok)
        self.QMessageBox.show()
        
    def windowsGroupBox(self):
        # Windows 10/11 Box
        self.windowsBox = QGroupBox("Windows 10/11", self.alertForm)
        self.windowsBox.setCheckable(True)
        notifications = self.settings.get_settings("notifications")
        self.windowsBox.setChecked(notifications.get("windows", {}).get("enabled", False))
        self.windowsBox.setStyleSheet("font-weight: bold;")
        windowsBoxLayout = QVBoxLayout()
        self.windowsBox.setLayout(windowsBoxLayout)
        self.alertForm.layout().addWidget(self.windowsBox)
     
    def telegramGroupBox(self):
        # Telegram Box
        self.telegramBox = QGroupBox("Telegram", self.alertForm)
        self.telegramBox.setCheckable(True)  
        notifications = self.settings.get_settings("notifications")
        self.telegramBox.setChecked(notifications.get("telegram", {}).get("enabled", False))
        self.telegramBox.setStyleSheet("font-weight: bold;")
        telegramBoxLayout = QVBoxLayout()
        self.telegramBox.setLayout(telegramBoxLayout)
        self.alertForm.layout().addWidget(self.telegramBox)
        
        # Telegram Chat ID
        telegramLayout = QHBoxLayout()
        telegramBoxLayout.addLayout(telegramLayout)
        telegramChatIdLabel = QLabel("chat_id: ", self.telegramBox)
        telegramLayout.addWidget(telegramChatIdLabel)
        self.telegramChatIdInput = QLineEdit(self.alertForm)
        self.telegramChatIdInput.setPlaceholderText("123456789")
        self.telegramChatIdInput.setText(notifications.get("telegram", {}).get("chat_id", ""))
        telegramLayout.addWidget(self.telegramChatIdInput)
        
        # Telegram Token
        telegramTokenLayout = QHBoxLayout()
        telegramBoxLayout.addLayout(telegramTokenLayout)
        telegramTokenLabel = QLabel("bot_token: ", self.telegramBox)
        telegramTokenLayout.addWidget(telegramTokenLabel)
        self.telegramTokenInput = QLineEdit(self.alertForm)
        self.telegramTokenInput.setPlaceholderText("123456789:ABCdefGHIjklMNoPQrSTUvWxYZ")
        self.telegramTokenInput.setText(notifications.get("telegram", {}).get("bot_token", ""))
        telegramTokenLayout.addWidget(self.telegramTokenInput)
    
    def discordGroupBox(self):
        # Discord webhook URL Box
        self.discordBox = QGroupBox("Discord", self.alertForm)
        self.discordBox.setCheckable(True)
        notifications = self.settings.get_settings("notifications")
        self.discordBox.setChecked(notifications.get("discord", {}).get("enabled", False))
        self.discordBox.setStyleSheet("font-weight: bold;")
        discordBoxLayout = QVBoxLayout()
        self.discordBox.setLayout(discordBoxLayout)
        self.alertForm.layout().addWidget(self.discordBox)
        
        # Discord webhook URL
        discordWebhookLayout = QHBoxLayout()
        discordBoxLayout.addLayout(discordWebhookLayout)
        discordWebhookLabel = QLabel("webhook_url: ", self.discordBox)
        discordBoxLayout.addWidget(discordWebhookLabel)
        self.discordWebhookInput = QLineEdit(self.alertForm)
        self.discordWebhookInput.setPlaceholderText("https://discord.com/api/webhooks/123456789/ABCdefGHIjklMNoPQrSTUvWxYZ")
        self.discordWebhookInput.setText(notifications.get("discord", {}).get("webhook_url", ""))
        discordBoxLayout.addWidget(self.discordWebhookInput)
        
    def ntfyshGroupBox(self):
        # Discord webhook URL Box
        self.ntfyBox = QGroupBox("Ntfy.sh", self.alertForm)
        self.ntfyBox.setCheckable(True)
        notifications = self.settings.get_settings("notifications")
        self.ntfyBox.setChecked(notifications.get("ntfy.sh", {}).get("enabled", False))
        self.ntfyBox.setStyleSheet("font-weight: bold;")
        ntfyBoxLayout = QVBoxLayout()
        self.ntfyBox.setLayout(ntfyBoxLayout)
        self.alertForm.layout().addWidget(self.ntfyBox)
        
        # Ntfy.sh webhook URL
        ntfyWebhookLayout = QHBoxLayout()
        ntfyBoxLayout.addLayout(ntfyWebhookLayout)
        ntfyWebhookLabel = QLabel("webhook_url: ", self.ntfyBox)
        ntfyBoxLayout.addWidget(ntfyWebhookLabel)
        self.ntfyWebhookInput = QLineEdit(self.alertForm)
        self.ntfyWebhookInput.setPlaceholderText("https://notify.run/123456789")
        self.ntfyWebhookInput.setText(notifications.get("ntfy.sh", {}).get("webhook_url", ""))
        ntfyBoxLayout.addWidget(self.ntfyWebhookInput)
        
       