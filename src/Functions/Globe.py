import json

class Globe():
    
    # Console
    console = None
    
    # Class properties
    type = None
    window_title = None
    properties = None
    
    def __init__(self, console, type, title, properties = dict()):
        # Log message
        self.console = console
        self.console.log(f"{__class__.__name__} initialization", "info")
        
        # Globe type
        self.type = type
        self.window_title = title
        self.properties = properties
        
        self.console.log(f"Globe type: {self.type} is being initialized", "info")
        
    def html_out(self):
        
        # Convert Python dict to JSON
        self.properties = json.dumps(self.properties, indent=4, sort_keys=True, default=int, ensure_ascii=False)
        
        html = f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Cesium Globe</title>
                    <link href="https://cdnjs.cloudflare.com/ajax/libs/cesium/1.103.0/Widgets/widgets.min.css" rel="stylesheet">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/cesium/1.103.0/Cesium.js"></script>
                    <style>
                        body {{
                            margin: 0;
                            padding: 0;
                        }}
                    </style>
                </head>
                <body>
                    <div id="cesiumContainer" style="height: 100vh !important;"></div>
                    <script> 
                        const viewer = new Cesium.Viewer("cesiumContainer", {self.properties});
                        var dataSource = new Cesium.CzmlDataSource();
                        viewer.dataSources.add(dataSource);
                        var proxy = "https://cors-anywhere.herokuapp.com/";
                        var czmlUrl = proxy + "https://sandcastle.cesium.com/SampleData/simple.czml";
                        dataSource.load(czmlUrl);
                    </script>
                </body>
            </html>
        '''
        return html
        
    def get_type(self):
        return self.type
    
    def get_window_title(self):
        return self.window_title