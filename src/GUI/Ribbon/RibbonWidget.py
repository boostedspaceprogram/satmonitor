from PyQt5.QtWidgets import *
from GUI.Ribbon.RibbonTab import RibbonTab
from GUI.Ribbon.StyleSheets import get_stylesheet

class RibbonWidget(QToolBar):
    def __init__(self, parent):
        QToolBar.__init__(self, parent)
        self.setStyleSheet(get_stylesheet("ribbon"))
        self.setObjectName("ribbonWidget")
        self.setWindowTitle("Ribbon")
        self._ribbon_widget = QTabWidget(self)
        self._ribbon_widget.setMaximumHeight(120)
        self._ribbon_widget.setMinimumHeight(110)
        self.setMovable(False)
        self.addWidget(self._ribbon_widget)

    def add_ribbon_tab(self, name):
        ribbon_tab = RibbonTab(self, name)
        ribbon_tab.setObjectName("tab_" + name)
        self._ribbon_widget.addTab(ribbon_tab, name)
        return ribbon_tab

    def set_active(self, name):
        self.setCurrentWidget(self.findChild("tab_" + name))