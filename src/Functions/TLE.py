import sys, time, json, requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread

class TLE(): 
    
    # Console
    console = None
    
    # Class variables
    url = None
    
    def __init__(self, console, url):
        # Log message
        self.console = console
        self.url = url
        self.console.log(f"{__class__.__name__} initialization", "info")
        self.console.log(f"{__class__.__name__} URL: {self.url}", "info")
    
    def TLE_data_request(self):
        TLEData = None
        request = requests.get(self.url)
        if request.status_code == 200:
            self.console.log(f"{__class__.__name__} data request success", "info")
            TLEData = request.text
        else:
            self.console.log(f"{__class__.__name__} data request failed", "error")
        return json.loads(TLEData)
    
    def TLETable(self):
        TLE_DATA = self.TLE_data_request()
        table = QTableWidget()
        # Set table properties
        for x, row in enumerate(TLE_DATA):
            table.setColumnCount(len(row))
            table.setRowCount(len(TLE_DATA))
            table.setHorizontalHeaderLabels(row.keys())
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            table.verticalHeader().setVisible(True)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            break
        
        # loop trough the TLE_DATA and add the data to the table widget
        for row, x in enumerate(TLE_DATA):
            for column, y in enumerate(x.values()):
                table.setItem(row, column, QTableWidgetItem(str(y)))
                
        return table