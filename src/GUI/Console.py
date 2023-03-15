from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QFrame, QTextEdit
import time

class Console():
    
    # Console properties
    conBgColor = "#000000" # hex background color
    conTextColor = "#FFFFFF" # hex text color
    conTextSize = 8 # pt size of text
    
    # Console types
    errTypes = ["error", "warning", "info", "debug"]
    errColors = ["red", "yellow", "lightblue", "purple"]
    
    # Console options
    prependDateTime = True # True = prepend date and time to message, False = don't prepend date and time to message
    doNotShowLogAfterType = 2 # 0 = error, 1 = warning, 2 = info, 3 = debug
    
    def __init__(self) -> None:
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
        
        # Console message
        self.log("Console class initialization", "info")
    
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
                if self.prependDateTime:
                    color = self.errColors[self.errTypes.index(type)]
                    self.console.append(time.strftime("%d/%m/%Y %H:%M:%S") + " <font color='" + color + "'>[" + type.upper() + "]</font> - " + text)
                else:
                    self.console.append("[" + type.upper() + "] - " + text)
        
    def clearText(self):
        self.console.clear()
    
    def showConsole(self):
        self.console.show()   
    
    def closeConsole(self):
        self.console.close()
        
    def refreshConsole(self):
        self.console.update()