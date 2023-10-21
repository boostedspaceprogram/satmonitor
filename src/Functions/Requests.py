import sys, time, json, requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread

class Requests():
    
    # Console
    console = None
    
    # Class variables
    url = None
    method = None
    headers = {}
    
    def __init__(self, console, url):
        # Log message
        self.console = console
        self.url = url
        self.console.log(f"{__class__.__name__} initialization", "info")
        self.console.log(f"{__class__.__name__} URL: {self.url}", "info")
        
    def set_url(self, url):
        self.url = url
        self.console.log(f"{__class__.__name__} URL: {self.url}", "debug")
        
    def set_method(self, method):
        self.method = method
        self.console.log(f"{__class__.__name__} URL: {self.url} Method set to {self.method.upper()}", "debug")
        
    def set_headers(self, headers):
        self.headers = headers
        self.console.log(f"{__class__.__name__} URL: {self.url} Headers set to {self.headers}", "debug")
        
    def make_requests(self):
        table = QTableWidget()
        request = requests.request(self.method, self.url, headers=self.headers)
        if request.status_code == 200:
            self.console.log(f"{__class__.__name__} [{self.method}] | URL: {self.url} | request success", "info")
        else:
            self.console.log(f"{__class__.__name__} [{self.method}] | URL: {self.url} | request failed", "error")
        return table