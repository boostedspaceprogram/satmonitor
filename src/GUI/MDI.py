from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium


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
        
        
        # Map sub window
        sub_window = QMdiSubWindow()
        folium_map = folium.Map(
            location=[45.372, -121.6972],
            zoom_start=1,
            tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga',
            attr='Google Imagery',
        )
        web_view = QWebEngineView()
        
        # web view no borders or scroll bars
        web_view.setContentsMargins(0, 0, 0, 0)
        web_view.setHtml(folium_map._repr_html_())
        sub_window.setWidget(web_view)
        self.mdiArea.addSubWindow(sub_window)
        sub_window.show()