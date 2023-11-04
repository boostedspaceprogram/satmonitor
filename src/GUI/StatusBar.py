import os, time, psutil

from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

from Functions.Settings import Settings


class StatusBar():
    
    currentTimeTimer = None
    console = None
    
    def __init__(self, console) -> None:
        # Console class
        self.console = console
        
        # settings class
        self.settings = Settings(self.console)
                
        # Console message
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # Status bar initailization/properties
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("QStatusBar::item { border: 0px solid black; }")
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setFixedHeight(20)
        self.statusBar.setContentsMargins(0, 0, 0, 0)
        
        # Version permanent widget bottom left
        self.app_version = QLabel()
        self.statusBar.deviderVersion = QLabel(" | ")
        self.statusBar.addWidget(self.app_version)
        self.statusBar.addWidget(self.statusBar.deviderVersion)
        
        # Time permanent widget
        self.current_datetime = QLabel()
        self.statusBar.deviderTime = QLabel(" | ")
        self.statusBar.addWidget(self.current_datetime)
        self.statusBar.addWidget(self.statusBar.deviderTime)
        
        # Status bar widget
        self.open()
        
    def open(self):
        # use QThread to get usage stats of CPU and RAM
        self.usage_thread = QThread()
        self.usage_thread.start()
        
        # Add App version to status bar (bottom left)
        self.show_app_version()
        
        # Add current time to status bar (bottom right)
        self.show_current_time()
        
        # Add CPU usage to status bar (bottom right)
        self.show_cpu_usage()
        
        # Add RAM usage to status bar (bottom right)
        self.show_ram_usage()
    
    def show_current_time(self):
        # create timer
        self.currentTimeTimer = QTimer()
        self.currentTimeTimer.timeout.connect(self.update_current_time)
        self.currentTimeTimer.start(1)
        
    def update_current_time(self):
        # update current time and date in format: DD/MM/YYYY HH:MM:SS and add indicator for Timezone
        self.current_datetime.setText(time.strftime("%d/%m/%Y %H:%M:%S") + " " + time.strftime("%Z"))  

    def show_app_version(self):
        # get app version from settings
        app_version = self.settings.get("version")
        
        # set app version to label
        self.app_version.setText("v" + app_version)
        
        
    def show_cpu_usage(self):
        self.cpu_usage_worker = CPUUsageWorker()
        self.cpu_usage_worker.moveToThread(self.usage_thread)
        self.cpu_usage_worker.cpu_usage_signal.connect(self.update_cpu_usage)
        self.cpu_usage_worker.start()
        
        # add CPU usage to status bar (bottom right) but on the left of current time
        self.cpu_usage = QLabel("CPU: 0%")
        self.statusBar.devider = QLabel(" | ")
        self.statusBar.addPermanentWidget(self.statusBar.devider)
        self.statusBar.addPermanentWidget(self.cpu_usage)
        
        # Console debug
        self.console.log("CPU usage thread started", "debug")
        
    def show_ram_usage(self):
        self.ram_usage_worker = RAMUsageWorker()
        self.ram_usage_worker.moveToThread(self.usage_thread)
        self.ram_usage_worker.ram_usage_signal.connect(self.update_ram_usage)
        self.ram_usage_worker.start()
        
        self.ram_usage = QLabel("RAM: 0%")
        self.statusBar.deviderRam = QLabel(" | ")
        self.statusBar.addPermanentWidget(self.statusBar.deviderRam)
        self.statusBar.addPermanentWidget(self.ram_usage)
        
        # Console debug
        self.console.log("RAM usage thread started", "debug")

    def update_cpu_usage(self, cpu_usage):
        self.cpu_usage.setText("CPU: {:.2f}%".format(cpu_usage))

    def update_ram_usage(self, ram_usage):
        # show RAM usage in percentage and MB
        self.ram_usage.setText("RAM: {:.2f}% ({:.2f} MB)".format(ram_usage, ram_usage * 1000))
        
    def appendText(self, text):
        """Append text to status bar

        Args:
            text (_type_): _description_
        """
        self.statusBar.showMessage(text)
        
    def clearText(self):
        """Clear text from status bar
        """
        self.statusBar.clearMessage()
        
class CPUUsageWorker(QThread):
    cpu_usage_signal = pyqtSignal(float)
        
    def run(self):
        p = psutil.Process(os.getpid())
        while True:
            cpu_percent = p.cpu_percent() / psutil.cpu_count()
            self.cpu_usage_signal.emit(cpu_percent)
            time.sleep(1)

class RAMUsageWorker(QThread):
    ram_usage_signal = pyqtSignal(float)
    
    def run(self):
        p = psutil.Process(os.getpid())
        while True:
            ram_percent = p.memory_percent()
            self.ram_usage_signal.emit(ram_percent)
            time.sleep(1)