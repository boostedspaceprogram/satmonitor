from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
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
        
        
        subwindow = QMdiSubWindow()
        subwindow.setWindowTitle("Cesium Globe")
        
        # Create a QWebEngineView widget
        self.webview = QWebEngineView()
        subwindow.setWidget(self.webview)
        
        # remove padding and margin from the QWebEngineView widget
        
        # Load the CesiumJS webpage
        self.webview.setHtml('''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Cesium Globe</title>
                    <link href="https://cdnjs.cloudflare.com/ajax/libs/cesium/1.103.0/Widgets/widgets.min.css" rel="stylesheet">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/cesium/1.103.0/Cesium.js"></script>
                    <style>
                        body {
                            margin: 0;
                            padding: 0;
                        }
                    </style>
                </head>
                <body>
                    <div id="cesiumContainer" style="height: 100vh !important;"></div>
                    <script> 
                        const viewer = new Cesium.Viewer("cesiumContainer", {
                            shouldAnimate: true,
                            homeButton: false,
                            navigationHelpButton: false,
                            timeline: false,
                            controls: false,
                        });
                        var dataSource = new Cesium.CzmlDataSource();
                        viewer.dataSources.add(dataSource);
                        var proxy = "https://cors-anywhere.herokuapp.com/";
                        var czmlUrl = proxy + "https://sandcastle.cesium.com/SampleData/simple.czml";
                        dataSource.load(czmlUrl);
                    </script>
                </body>
            </html>
        ''')
        
        # set cors policy
        
        
        # Add the QMdiSubWindow to the QMdiArea
        self.mdiArea.addSubWindow(subwindow)