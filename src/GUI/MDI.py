from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit, QStatusBar
from PyQt5.QtCore import QTimer
import os, time

class MDI():
    
    console = None
    
    def __init__(self, console):
        # Console class
        self.console = console
        
        # Console message
        self.console.log("MDI class initialization", "info")
        
        # MDI initialization/properties
        self.mdiArea = QMdiArea() 
        
        # Status bar widget
        self.open()
        
    def open(self):
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