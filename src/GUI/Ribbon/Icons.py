from PyQt5.QtGui import *
import os

icons_instance = None
srcPath = ""


def get_icon(name):
    global icons_instance
    if not icons_instance:
        icons_instance = Icons()
    return icons_instance.icon(name)


class Icons(object):
    def __init__(self):
        self.srcPath = os.path.dirname(os.path.realpath(__file__))
        
        self._icons = {}
        self.make_icon("settings", "icons/settings.png")
        self.make_icon("logo", "icons/logo.png")
        self.make_icon("tools", "icons/tools.png")
        self.make_icon("console", "icons/console.png")
        self.make_icon("console_disabled", "icons/console_disabled.png")
        self.make_icon("refresh", "icons/refresh.png")
        self.make_icon("grid_tile", "icons/grid_tile.png")
        self.make_icon("grid_cascade", "icons/grid_cascade.png")
        self.make_icon("grid_close_all", "icons/grid_close_all.png")
        self.make_icon("alert", "icons/alert.png")
        self.make_icon("alert_mute", "icons/alert_mute.png")
        self.make_icon("tle_view", "icons/tle_view.png")
        
        # Default fallback icon
        self.make_icon("default", "icons/default.png")

    def make_icon(self, name, path):
        icon = QIcon()
        icon.addPixmap(QPixmap(self.srcPath + "/" + path), QIcon.Normal, QIcon.Off)
        self._icons[name] = icon

    def icon(self, name):
        icon = self._icons["default"]
        try:
            icon = self._icons[name]
        except KeyError:
            print("icon " + name + " not found")
        return icon
