from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import *
import time

class Console():
    
    # Console properties
    conBgColor = "#000000" # hex background color
    conTextColor = "#FFFFFF" # hex text color
    conTextSize = 8 # pt size of text
    conCurrFilter = ["info"]
    
    # Console types
    errTypes = ["info", "warning", "error", "debug"]
    errTypesColors = ["white", "yellow", "red", "purple"]
    errColors = ["white", "yellow", "red", "green"]
    
    # Console options
    prependDateTime = True # True = prepend date and time to message, False = don't prepend date and time to message
    doNotShowLogAfterType = 3 # 0 = info, 1 = warning, 2 = error, 3 = debug
    
    # Console log messages
    consoleLogMessages = []
    
    def __init__(self) -> None:
        # Grid where console is placed in with filter buttons
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)
        
        # Filter buttons inside QHBoxLayout
        self.filterButtons = QHBoxLayout()
        self.filterButtons.setContentsMargins(0, 0, 0, 0)
        self.filterButtons.setSpacing(1)
        
        # Filter buttons
        # Info button
        self.filterInfo = QPushButton("Info")
        self.filterInfo.setCheckable(True)
        self.filterInfo.setChecked(True)
        self.filterInfo.clicked.connect(lambda: self.addFilter("info"))
        self.filterInfo.setStyleSheet("background-color: " + self.errTypesColors[self.errTypes.index("info")] + "; font-weight: bold;")
        
        # Warning button
        self.filterWarning = QPushButton("Warning")
        self.filterWarning.setCheckable(True)
        self.filterWarning.setChecked(False)
        self.filterWarning.clicked.connect(lambda: self.addFilter("warning"))
        self.filterWarning.setStyleSheet("background-color: " + self.errTypesColors[self.errTypes.index("warning")] + "; font-weight: bold;")
        
        # Error button
        self.filterError = QPushButton("Error")
        self.filterError.setCheckable(True)
        self.filterError.setChecked(False)
        self.filterError.clicked.connect(lambda: self.addFilter("error"))
        self.filterError.setStyleSheet("background-color: " + self.errTypesColors[self.errTypes.index("error")] + "; font-weight: bold;")
        
        # Debug button
        self.filterDebug = QPushButton("Debug")
        self.filterDebug.setCheckable(True)
        self.filterDebug.setChecked(False)
        self.filterDebug.clicked.connect(lambda: self.addFilter("debug"))
        self.filterDebug.setStyleSheet("background-color: " + self.errTypesColors[self.errTypes.index("debug")] + "; font-weight: bold;")
        
        # Add filter buttons to filterButtons
        self.filterButtons.addWidget(self.filterInfo)
        self.filterButtons.addWidget(self.filterWarning)
        self.filterButtons.addWidget(self.filterError)
        self.filterButtons.addWidget(self.filterDebug)
            
        # Add filter buttons to grid
        self.grid.addLayout(self.filterButtons, 0, 0)
        
        # Console initialization/properties
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setUndoRedoEnabled(False)
        self.console.setAcceptRichText(False)
        self.console.setContextMenuPolicy(Qt.NoContextMenu)
        self.console.setFrameStyle(QFrame.NoFrame)
        self.console.setTabStopWidth(4)
        self.console.setWordWrapMode(QTextOption.NoWrap)
        self.console.setTabChangesFocus(True)
        self.console.setAcceptDrops(False)
        self.console.setStyleSheet("background-color: " + self.conBgColor + "; color: " + self.conTextColor + "; font-size: " + str(self.conTextSize) + "pt; font-family: 'Courier New';")
        
        # Add console to grid
        self.grid.addWidget(self.console, 1, 0)
        
        # Create widget for hole grid and set layout
        self.gridWidget = QWidget()
        self.gridWidget.setLayout(self.grid)
        
        # Console message
        self.log(f"{__class__.__name__} initialization", "info")
    
    def checkTypes(self, types):
        # Check if given type is valid and return True or False
        if types in self.errTypes:
            return True
        else:
            return False
    
    def log(self, text, type): 
        # Check if type is valid
        if not self.checkTypes(type):
            self.console.append("Error - Invalid type: " + type)
        else:
            if self.errTypes.index(type) <= self.doNotShowLogAfterType:
                typeColor = self.errTypesColors[self.errTypes.index(type)]
                color = self.errColors[self.errTypes.index(type)]
                if self.prependDateTime:
                    # Add message to consoleLogMessages list
                    self.consoleLogMessages.append({
                        "type": type,
                        "text": " <font color='" + typeColor + "'>[" + type.upper() + "]</font> <font color='" + color + "'>" + text + "</font>",
                        "time": time.strftime("%d/%m/%Y %H:%M:%S"),
                        "appendTime": self.prependDateTime
                    })
                    
                    # Show filtered console
                    self.showFilteredConsole()
                else:
                    # Add message to consoleLogMessages queue list
                    self.consoleLogMessages.append({
                        "type": type,
                        "text": " <font color='" + typeColor + "'>[" + type.upper() + "]</font> <font color='" + color + "'>" + text + "</font>",
                        "time": time.strftime("%d/%m/%Y %H:%M:%S"),
                        "appendTime": self.prependDateTime
                    })
                    
                    # Show filtered console
                    self.showFilteredConsole()
        
    def clearText(self):
        self.console.clear()
    
    def showConsole(self):
        self.console.show()   
    
    def closeConsole(self):
        self.console.close()
        
    def refreshConsole(self):
        self.console.update()
    
    def addFilter(self, type):
        # Add or remove type to list of filters
        if type not in self.conCurrFilter:
            self.conCurrFilter.append(type)
        else:
            self.conCurrFilter.remove(type)
            
        # Show filtered console
        self.showFilteredConsole()
            
    def showFilteredConsole(self):
        # TODO: Show filtered console based on conCurrFilter and consoleLogMessages list
        self.clearText()
        
        # Variable for storing messages that wil later be filtered on time
        unfilteredTimeMessages = []
        
        # Check which filters are current active
        for filter in self.conCurrFilter:
            for message in self.consoleLogMessages:
                if message["type"] == filter:
                    if message["appendTime"]:
                        unfilteredTimeMessages.append(message["time"] + message["text"])
                    else:
                        unfilteredTimeMessages.append(message["text"])
                        
        # Sort messages on time ascending
        unfilteredTimeMessages.sort()
        
        # Add messages to console
        for message in unfilteredTimeMessages:
            self.console.append(message)
        
        # Refresh console
        self.refreshConsole()