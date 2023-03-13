from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from GUI.Ribbon.StyleSheets import get_stylesheet

class RibbonButton(QToolButton):
    def __init__(self, owner, action, is_large):
        QPushButton.__init__(self, owner)
        self._actionOwner = action
        self.update_button_status_from_action()
        self.clicked.connect(self._actionOwner.trigger)
        self._actionOwner.changed.connect(self.update_button_status_from_action)

        if is_large:
            self.setMaximumWidth(80)
            self.setMinimumWidth(50)
            self.setMinimumHeight(75)
            self.setMaximumHeight(80)
            self.setStyleSheet(get_stylesheet("ribbonButton"))
            self.setToolButtonStyle(3)
            self.setIconSize(QSize(32, 32))
        else:
            self.setToolButtonStyle(2)
            self.setMaximumWidth(120)
            self.setIconSize(QSize(16, 16))
            self.setStyleSheet(get_stylesheet("ribbonSmallButton"))

    def update_button_status_from_action(self):
        self.setText(self._actionOwner.text())
        self.setStatusTip(self._actionOwner.statusTip())
        self.setToolTip(self._actionOwner.toolTip())
        self.setIcon(self._actionOwner.icon())
        self.setEnabled(self._actionOwner.isEnabled())
        self.setCheckable(self._actionOwner.isCheckable())
        self.setChecked(self._actionOwner.isChecked())
