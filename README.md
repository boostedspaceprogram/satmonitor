# Sat-Monitor [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fboostedspaceprogram%2Fsatmonitor&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=hits&edge_flat=true)](https://hits.seeyoufarm.com) ![GitHub](https://img.shields.io/github/license/boostedspaceprogram/satmonitor) ![GitHub issues](https://img.shields.io/github/issues/boostedspaceprogram/satmonitor) ![GitHub pull requests](https://img.shields.io/github/issues-pr/boostedspaceprogram/satmonitor) ![GitHub contributors](https://img.shields.io/github/contributors/boostedspaceprogram/satmonitor) ![GitHub last commit](https://img.shields.io/github/last-commit/boostedspaceprogram/satmonitor) [![Compile & Compress - Windows](https://github.com/boostedspaceprogram/satmonitor/actions/workflows/compile-and-compress-windows.yml/badge.svg)](https://github.com/boostedspaceprogram/satmonitor/actions/workflows/compile-and-compress-windows.yml) ![GitHub Repo stars](https://img.shields.io/github/stars/boostedspaceprogram/satmonitor?style=social) ![GitHub watchers](https://img.shields.io/github/watchers/boostedspaceprogram/satmonitor?style=social) ![GitHub forks](https://img.shields.io/github/forks/boostedspaceprogram/satmonitor?style=social)

Satellite Monitoring system for the Boosted Space Program (BSP) project. 
Get real time data from the satellites and visualize it inside a MDI (Multiple Document Interface) application for easy access to multiple different data sources at the same time.

# About BSP
The Boosted Space Program (BSP) is a project that aims to create a community of space enthusiasts and professionals to work together on a variety of space projects. The 'Sat-Monitor' project is currently in its early stages, but we are working hard to make it a reality.

## Table of Contents
- [Features](#features)
- [How to build and run on Windows](#how-to-build-and-run-on-windows-/-macos-/-linux)
- [Contributing](#contributing)
- [License](#license)

## Features
Here is a list of the features that we want to implement in the application. When a particular feature is implemented, it will be marked with a checkmark. If you want to contribute to the project, you can check the issues tab and see if there are any features that you can implement. If you have any questions, feel free to ask in the issues tab.

#### MUST HAVE
- [ ] Track satellites and other space objects in real time
- [ ] Visualization of the satellites' orbits and positions in 3D
- [ ] Controls for the visualization (zoom, rotate, etc.)
- [ ] Display of the satellites' telemetry data (altitude, velocity, etc.)
- [ ] Display of the satellites' images and 3D models (if available)

#### SHOULD HAVE
- [ ] Ability to view ongoing and upcoming missions and their details
- [ ] Live video feed of ongoing missions (if available)
- [ ] Notifications for upcoming events (launches, landings, etc.)

#### COULD HAVE
- [ ] Live radio SDR (Software Defined Radio) feed and frequencies of the satellites (if available)
- [ ] Push notifications for upcoming events (launches, landings, etc.) to mobile devices

#### WON'T HAVE
- [X] Paid subscription, ads, or any other form of monetization, unless it is for a good cause. ❤️🚀

## How to build and run on Windows / MacOS / Linux
1. Install python3 and pip3
2. Install requirements: `pip3 install -r requirements.txt`
3. Run the following command: `pyinstaller Sat-Monitor.spec` on the OS that you want to build for (Windows, MacOS, Linux)
4. Run the executable called `Sat-Monitor` in the `dist` folder

## Contributing
1. Fork it (<https://github.com/boostedspaceprogram/satmonitor>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request (PR) with a detailed description of the changes and correct labels.
6. Wait for a review and approval from a maintainer.

## License
This project is licensed under the GNu General Public License v3.0 - see the [LICENSE](LICENSE) file for details. 
TLDR: You can use this project for any purpose, but you must publish your changes under the same license. 
