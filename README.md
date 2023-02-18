# BulkUpdate

Update your android device fleet at once

Bulkupdate is a small script which automatically downloads the latest versions and installs them on your devices via adb. You can lean back and relax as long as you like

  

# Installation

1. Clone this repo ```git clone https://github.com/SpielerNogard/Bulkupdate.git```

2. Install the requirements
	- Best practice is to create a virtual env ```python -m venv .venv```
	- ```pip install -r requirements.txt```
3. Check if ADB is installed
	- on Windows you can use the adb.zip file, extract it to this folder
	- in MAC OS ```brew install android-platform-tools```
	- in Linux ```sudo apt-get install adb```
4. Insert your devices in devices.json
	1. Device with name: ```{"192.168.178.20":{"name":"my fancy name"}}```
	2. Device without name: ```{"192.168.178.20":{}}```
	3. Your file should lock something like this (add as much devices as you like)
		```
		{"192.168.178.20":{},
		 "192.168.178.21":{"name":"my fancy name"}}
		```
5. Start Bulkupdate ```python main.py```

# Notes
The APKMirror download code is inspired by `APKMirror-Search 1.0.0`  can be downloaded here: `https://pypi.org/project/APKMirror-Search/`

# TODOs
- [ ] AutoDetect compatible devices in network 