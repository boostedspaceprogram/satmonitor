# satmonitor
Satellite Monitoring system

## How to build and run
1. Install python3 and pip3
2. Install requirements: `pip3 install -r requirements.txt`
3. Run the following command: `pyinstaller --noconsole --onefile --name "Sat-Monitor" --add-data="src/GUI/Ribbon/icons;GUI/Ribbon/icons" --add-data="src/GUI/Ribbon/stylesheets;GUI/Ribbon/stylesheets" src/main.py`
4. Run the executable in the `dist` folder