import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from GUI.MainWindow import MainWindow
from GUI.Console import Console
from GUI.Ribbon.Icons import get_icon
from Functions.Settings import Settings
from qt_material import apply_stylesheet

try:
    from ctypes import windll  # Only exists on Windows.
    appId = 'boostedspaceprogram.satmonitor'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
except ImportError:
    pass

def main():
    # Create app and main window
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Prevent app from closing when last window is closed, instead hide to system tray 
    main_window = MainWindow()
    
    # Classes
    console = Console()
    settings = Settings(console)
    
    # Set theme
    theme = settings.get_settings("theme") or "default"
    
    # Check if theme is not default
    if theme != "default":
        apply_stylesheet(app, theme=theme)
    
    # Tray handler
    icon = QIcon(get_icon("logo_dark"))
    
    # Adding item on the menu bar 
    tray = QSystemTrayIcon() 
    tray.setIcon(icon) 
    tray.setVisible(True) 
    tray.setToolTip("Sat Monitor")
    
    # Listen for double-click on tray icon
    def tray_double_clicked(reason):
        if reason == QSystemTrayIcon.DoubleClick:
            main_window.show()

    tray.activated.connect(tray_double_clicked)
    
    # Creating the options 
    menu = QMenu() 
    
    # Name 
    name = QAction("Sat Monitor")
    name.setEnabled(False)
    name.setIcon(icon)
    menu.addAction(name)
    
    # Open
    optionShowApp = QAction("Open") 
    optionShowApp.triggered.connect(main_window.show)
    menu.addAction(optionShowApp)
    
    # Quit 
    quit = QAction("Quit") 
    quit.triggered.connect(app.quit) 
    menu.addAction(quit) 
    
    # Adding options to the System Tray 
    tray.setContextMenu(menu) 
    
    # Show main window and execute app
    main_window.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
