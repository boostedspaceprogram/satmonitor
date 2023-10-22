import sys
from PyQt5.QtWidgets import *
from GUI.MainWindow import MainWindow
from GUI.Console import Console
from Functions.Settings import Settings
from qt_material import apply_stylesheet

def main():
    # Create app and main window
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    main_window = MainWindow()
    
    # Create console
    console = Console()
    
    # Load theme from settings.json
    settings = Settings(console)
    theme = settings.get_settings()["theme"] or "default"
    
    # Check if theme is not default
    if theme != "default":
        apply_stylesheet(app, theme=theme)
    
    # Show main window and execute app
    main_window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
