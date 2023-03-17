from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
        # Globe sub window
        globe_3d_subwindow = QMdiSubWindow()
        globe_3d_subwindow.setWindowTitle("Cesium Globe")
        
        # Create a QWebEngineView widget
        self.WebView3D = QWebEngineView()
        globe_3d_subwindow.setWidget(self.WebView3D)
        
        # Load the CesiumJS webpage
        self.WebView3D.setHtml('''
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
        
        self.mdiArea.addSubWindow(globe_3d_subwindow)
        
        
        # 2D Globe sub window
        globe_2d_subwindow = QMdiSubWindow()
        globe_2d_subwindow.setWindowTitle("2D Globe")
        
        # Create a QWebEngineView widget
        self.WebView2D = QWebEngineView()
        globe_2d_subwindow.setWidget(self.WebView2D)
        
        # Load the CesiumJS webpage
        self.WebView2D.setHtml('''
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
                            sceneMode: Cesium.SceneMode.SCENE2D,
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
        
        self.mdiArea.addSubWindow(globe_2d_subwindow)

       