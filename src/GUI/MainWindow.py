from PyQt5.QtCore import *
from GUI.Ribbon.RibbonButton import RibbonButton
from GUI.Ribbon.Icons import get_icon
from GUI.Ribbon.RibbonWidget import *
from GUI.StatusBar import StatusBar
from GUI.MDI import MDI
from GUI.Console import Console

# Widgets
from GUI.Widgets.About import *

class MainWindow(QMainWindow):
    
    console = None
    
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.resize(1280, 720)
        self.setWindowTitle("Home - Sat Monitor")
        self.setWindowIcon(get_icon("logo_dark"))
        self.setDockNestingEnabled(True)

        # Console class
        self.console = Console()
        
        # MDI class
        self.mdiArea = MDI(self.console)
        self.setCentralWidget(self.mdiArea.mdiArea)
        
        # load status bar from StatusBar.py
        self.statusBar = StatusBar(self.console)
        self.setStatusBar(self.statusBar.statusBar)
        
        # create bottom dock widget and add console to it
        self.consoleDock = QDockWidget("Console", self)
        self.consoleDock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.consoleDock.setWidget(self.console.gridWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.consoleDock)
        self.consoleDock.setTitleBarWidget(QWidget())
        self.consoleDock.hide()
        
        # -------------        actions       -----------------
        # Home tab
        self._refresh_action = self.add_action("Refresh", "refresh", "Refresh", True, self.on_refresh)
        self._grid_tile = self.add_action("Tile", "grid_tile", "Tile", True, self.on_grid_tile)
        self._grid_cascade = self.add_action("Cascade", "grid_cascade", "Cascade", True, self.on_grid_cascade)
        self._grid_close_all = self.add_action("Close all", "grid_close_all", "Close all", True, self.on_grid_close_all)
        self._alert_action = self.add_action("Alerts", "alert", "Alerts", True, self.on_alert)
        self._alert_mute = self.add_action("Mute", "alert_mute", "Mute", True, self.on_alert_mute)
        self._open_about = self.add_action("About", "about", "About", True, self.on_open_about)
        
        # Settings tab
        self._open_settings = self.add_action("Settings", "settings", "Open settings", True, self.on_open_settings) 
        self._open_console = self.add_action("Open console", "console", "Open console", True, self.on_open_console)
        self._close_console = self.add_action("Close console", "console", "Close console", True, self.on_close_console)
        self._close_console.setEnabled(False)
        
        # Flight tab
        self._open_live_flight = self.add_action("Live Flight", "default", "Open Live Flight", True, self.on_open_live_flight)
        
        # Satellite tab
        self._open_upcoming_launches = self.add_action("Upcoming Launches", "default", "Open Upcoming Launches", True, self.on_open_upcoming_launches)

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
        home_tab = self._ribbon.add_ribbon_tab("Home")
        home_pane = home_tab.add_ribbon_pane("Home")
        grid_pane = home_tab.add_ribbon_pane("Grid")
        alert_pane = home_tab.add_ribbon_pane("Alerts")
        help_pane = home_tab.add_ribbon_pane("Help")
        
        # Home pane
        home_pane.add_ribbon_widget(RibbonButton(self, self._refresh_action, True))
        
        # Grid pane
        grid_pane.add_ribbon_widget(RibbonButton(self, self._grid_tile, True))
        grid_pane.add_ribbon_widget(RibbonButton(self, self._grid_cascade, True))
        grid_pane.add_ribbon_widget(RibbonButton(self, self._grid_close_all, True))
        
        # Alert pane
        alert_pane.add_ribbon_widget(RibbonButton(self, self._alert_action, True))
        alert_pane.add_ribbon_widget(RibbonButton(self, self._alert_mute, True))
        
        # Flight Tab
        flight_tab = self._ribbon.add_ribbon_tab("Flight")
        flight_pane = flight_tab.add_ribbon_pane("Flight")
        flight_pane.add_ribbon_widget(RibbonButton(self, self._open_live_flight, True))
        
        # Satellite Tab
        satellite_tab = self._ribbon.add_ribbon_tab("Satellite")
        satellite_pane = satellite_tab.add_ribbon_pane("Satellite")
        satellite_pane.add_ribbon_widget(RibbonButton(self, self._open_upcoming_launches, True))
        
        # Help pane
        help_pane.add_ribbon_widget(RibbonButton(self, self._open_about, True))
        
        # System Tab
        system_tab = self._ribbon.add_ribbon_tab("System")
        configuration_pane = system_tab.add_ribbon_pane("Configuration")
        configuration_pane.add_ribbon_widget(RibbonButton(self, self._open_settings, True))
        
        console_pane = system_tab.add_ribbon_pane("Console")
        console_pane.add_ribbon_widget(RibbonButton(self, self._open_console, True))
        console_pane.add_ribbon_widget(RibbonButton(self, self._close_console, True))
    
    def on_open_live_flight(self):
        self.console.log("Live Flight opened", "debug")
        return None
        
    def on_open_about(self):
        self.console.log("About opened", "debug")
        self.mdiArea.AboutWindow()
        
    def on_open_upcoming_launches(self):
        self.console.log("Upcoming Launches opened", "debug")
        self.mdiArea.upcomingLaunchesWindow().show()
        
    def on_open_settings(self):
        self.console.log("Settings opened", "debug")
        self.mdiArea.settingsWindow().show()
        pass
    
    def on_open_console(self):
        if self.consoleDock.isVisible():
            return
        self.console.log("Console opened", "debug")
        self.consoleDock.show()
        self._open_console.setEnabled(False)
        self._close_console.setEnabled(True)
        
    def on_close_console(self):
        if not self.consoleDock.isVisible():
            return
        self.console.log("Console closed", "debug")
        self.consoleDock.hide()
        self._open_console.setEnabled(True)
        self._close_console.setEnabled(False)
        
    def on_refresh(self):
        pass
    
    def on_grid_tile(self):
        self.mdiArea.mdiArea.tileSubWindows()
        
    def on_grid_cascade(self):
        self.mdiArea.mdiArea.cascadeSubWindows()
        
    def on_grid_close_all(self):
        self.mdiArea.mdiArea.closeAllSubWindows()
        
    def on_alert(self):
        self.mdiArea.alertWindow().show()

    def on_alert_mute(self):
        pass