from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence as QKSec
from GUI.Ribbon.RibbonButton import RibbonButton
from GUI.Ribbon.Icons import get_icon
from GUI.Ribbon.RibbonTextbox import RibbonTextbox
from GUI.Ribbon.RibbonWidget import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.resize(1280, 720)
        self.setWindowTitle("Main Window")
        self.setDockNestingEnabled(True)
        self.setWindowIcon(get_icon("logo"))
        
        # create MDI area
        self.mdiArea = QMdiArea()
        
        # set the central widget
        self.setCentralWidget(self.mdiArea)
        
        # status bar
        self.statusBar().showMessage("Loaded ...")
        
        # add mdi sub window
        sub = QMdiSubWindow()
        sub.setWidget(QTextEdit())
        self.mdiArea.addSubWindow(sub)
        sub.show()
        
        # add mdi sub window
        sub2 = QMdiSubWindow()
        sub2.setWidget(QTextEdit())
        self.mdiArea.addSubWindow(sub2)
        sub2.show()
        
        # -------------        actions       -----------------

        self._open_settings = self.add_action("Settings", "settings", "Open settings", True, self.on_open_settings)
        self._open_tools = self.add_action("Tools", "tools", "Open tools", True, self.on_open_tools)
        
        # -------------      end actions       -----------------

        # Ribbon

        self._ribbon = RibbonWidget(self)
        self.addToolBar(self._ribbon)
        self.init_ribbon()            

    def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
        action = QAction(get_icon(icon_name), caption, self)
        action.setStatusTip(status_tip)
        action.triggered.connect(connection)
        action.setIconVisibleInMenu(icon_visible)
        if shortcut is not None:
            action.setShortcuts(shortcut)
        self.addAction(action)
        return action

    def init_ribbon(self):
        # -------------      ribbon       -----------------
        system_tab = self._ribbon.add_ribbon_tab("System")
        configuration_pane = system_tab.add_ribbon_pane("Configuration")
        configuration_pane.add_ribbon_widget(RibbonButton(self, self._open_settings, True))
        configuration_pane.add_ribbon_widget(RibbonButton(self, self._open_tools, True))

    def on_open_settings(self):
        pass
    
    def on_open_tools(self):
        pass