import requests
import pyfiglet
import urllib
import json
from Updater import Bulkupdate
class BulkupdateUpdater(object):
    def __init__(self):
        ascii_banner = pyfiglet.figlet_format("BulkUpdate")
        print(ascii_banner)

        self.Server = "http://157.90.184.181/"
        url = self.Server + "Version2.json"
        r = requests.get(url)
        Ergebnis = r.json()
        self.Version = Ergebnis['BulkVersion']
        self.find_installed_version()
        self.update()
        self.Bulkupdate = Bulkupdate()

    def update(self):
        if self.Version != self.current_installed:
            print("New Version avaible start updating")
            urllib.request.urlretrieve ("http://157.90.184.181/uploads/Updater.py", "Updater.py")
            urllib.request.urlretrieve ("http://157.90.184.181/uploads/Version.json", "Version.json")
            urllib.request.urlretrieve ("http://157.90.184.181/uploads/config.py", "config.py")
            print("Update done")
        else:
            print("Your Bulkupdate is up to date")

    def find_installed_version(self):
        f = open('Version.json',)
        data = json.load(f)
        self.current_installed = data['Version']
        f.close()

if __name__ == "__main__":
    Bulkupdate = BulkupdateUpdater()
