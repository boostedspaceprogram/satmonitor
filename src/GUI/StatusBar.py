from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import os, time, psutil

class StatusBar():
    
    currentTimeTimer = None
    console = None
    
    def __init__(self, console) -> None:
        # Console class
        self.console = console
                
        # Console message
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # Status bar initailization/properties
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("QStatusBar::item { border: 0px solid black; }")
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setFixedHeight(20)
        self.statusBar.setContentsMargins(0, 0, 0, 0)
        
        # Time permanent widget
        self.current_datetime = QLabel()
        self.statusBar.addPermanentWidget(self.current_datetime)
        
        # Status bar widget
        self.open()
        
    def open(self):
        # Add current time to status bar (bottom right)
        self.show_current_time()
        
        # use QThread to get usage stats of CPU and RAM
        self.usage_thread = QThread()
        self.usage_thread.start()
        
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
        self.statusBar.addPermanentWidget(self.ram_usage)
        
        # Console debug
        self.console.log("RAM usage thread started", "debug")

    def update_cpu_usage(self, cpu_usage):
        # update CPU usage in status bar
        self.cpu_usage.setText("CPU: " + str(cpu_usage) + "%")
        
    def update_ram_usage(self, ram_usage):
        # update RAM usage in status bar
        self.ram_usage.setText("RAM: " + str(ram_usage) + "%")
        
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
    cpu_usage_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            self.cpu_usage_signal.emit(self.get_cpu_usage())
            time.sleep(1)
            
    def get_cpu_usage(self):
        # get average CPU usage of program from 0 to 100 percent
        return psutil.cpu_percent()
    
class RAMUsageWorker(QThread):
    ram_usage_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            self.ram_usage_signal.emit(self.get_ram_usage())
            time.sleep(1)
            
    def get_ram_usage(self):
        # get RAM usage of program from 0 to 100 percent
        p = psutil.Process(os.getpid())
        return p.memory_percent()
        