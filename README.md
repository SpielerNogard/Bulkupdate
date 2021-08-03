

# BulkUpdate
Update your MAD devices automatically
  
Bulkupdate is a small script which automatically downloads the latest versions and installs them on your devices via adb. You can lean back and relax as long as you like
## V1.0.0
- Added auto update for the script
- Added PogoDroid to own Server
- Added Support for 32 bit
- Added config file for own usage

## V1.0.1
- disabled clear_folder, because errors
- some minor fixes

## V1.0.2
- Clear Folder now fixed
- Autoupdate fixed
- 
You need to use git pull this time, to get the actual update. Next time the autoupdate will work.
## Installation

1. Clone the repository
````
git clone https://github.com/SpielerNogard/Bulkupdate.git
````
2. Switch into Bulkupdate folder
````
cd Bulkupdate
````
3. install all requirements
````
pip3 install -r requirements.txt
````

## Usage

1. Start Bulkupdate
````
python3 BulkUpdate.py
````

This will update the BulkUpdate first if necessary. Then the program starts and you can select the functions

## Functions
1. List all your Devices
2. add IP Adresses to your list of Devices ( 64bit ) (necessary before first use)
3. add IP Adresses to your list of Devices ( 32bit ) (necessary before first use)
4. Update PoGo to latest supported Version
5. Update Pogo to latest stable Version ( used for downgrade, this will uninstall Pogo first)
6. Updating PogoDroid
7. Update both ( experimental)
