from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import os, time

class StatusBar():
    
    currentTimeTimer = None
    console = None
    
    def __init__(self, console) -> None:
        # Console class
        self.console = console
                
        # Console message
        self.console.log("StatusBar class initialization", "info")
        
        # Status bar initailization/properties
        self.statusBar = QStatusBar()
        self.statusBar.setObjectName("statusBar")
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
        
        # Add CPU usage to status bar (bottom right)
        self.show_cpu_usage()
    
    def show_current_time(self):
        # create timer
        self.currentTimeTimer = QTimer()
        self.currentTimeTimer.timeout.connect(self.update_current_time)
        self.currentTimeTimer.start(1)
        
    def update_current_time(self):
        # update current time and date in format: DD/MM/YYYY HH:MM:SS and add indicator for Timezone
        self.current_datetime.setText(time.strftime("%d/%m/%Y %H:%M:%S") + " " + time.strftime("%Z"))  

    def show_cpu_usage(self):
        # use QThread to get CPU usage
        self.cpu_usage_thread = QThread()
        self.cpu_usage_thread.start()
        self.cpu_usage_worker = CPUUsageWorker()
        self.cpu_usage_worker.moveToThread(self.cpu_usage_thread)
        self.cpu_usage_worker.cpu_usage_signal.connect(self.update_cpu_usage)
        self.cpu_usage_worker.start()

        # add CPU usage to status bar (bottom right) but on the left of current time
        self.cpu_usage = QLabel("CPU: 0%")
        self.statusBar.addPermanentWidget(self.cpu_usage)

    def update_cpu_usage(self, cpu_usage):
        # update CPU usage in status bar
        self.console.log("Thread started new CPU usage", "debug")
        self.cpu_usage.setText("CPU: " + str(cpu_usage) + "%")
        self.console.log("CPU: " + str(cpu_usage) + "%", "debug")
        self.console.log("Thread finished getting new CPU usage", "debug")
        
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
        # get CPU usage
        return int(os.popen('wmic cpu get loadpercentage').read().split()[1])