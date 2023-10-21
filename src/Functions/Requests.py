import time, requests, requests_cache
from datetime import timedelta
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
    timeout = 30
    disableCache = False
    
    # Requests cache
    session = requests_cache.CachedSession(
        'cache',
        backend='sqlite',
        cache_control=True,                # Use Cache-Control response headers for expiration, if available
        expire_after=timedelta(minutes=30),    # Otherwise expire responses after one day
        allowable_codes=[200, 400],        # Cache 400 responses as a solemn reminder of your failures
        allowable_methods=['GET', 'POST'], # Cache whatever HTTP methods you want
        ignored_parameters=['api_key'],    # Don't match this request param, and redact if from the cache
        stale_if_error=True,               # In case of request errors, use stale cache data if possible
    )
    
    def __init__(self, console, url, disable_cache=False):
        # Log message
        self.console = console
        self.url = url
        self.disableCache = disable_cache
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
        
    def set_timeout(self, timeout):
        self.timeout = timeout
        self.console.log(f"{__class__.__name__} URL: {self.url} Timeout set to {self.timeout}", "debug")
        
    def get_cache_info(self):
        return self.session.cache
        
    def make_requests(self):
        if self.disableCache:
            with requests_cache.disabled():
                t = time.time()
                request = self.session.request(self.method, self.url, headers=self.headers, timeout=self.timeout)
        else:
            t = time.time()
            request = self.session.request(self.method, self.url, headers=self.headers, timeout=self.timeout)
                
        if request.status_code == 200:
            self.console.log(f"{__class__.__name__} [{self.method}] | URL: {self.url} | Request success | MS: {round((time.time() - t) * 1000)}", "debug")
            return request.json()
        else:
            self.console.log(f"{__class__.__name__} [{self.method}] {request.status_code} | URL: {self.url} | Request failed | MS: {round((time.time() - t) * 1000)}", "error")
            return None # Return None if request failed
            