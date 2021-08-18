import requests
import os
import zipfile
import glob

import config

class Downloader(object):
    def __init__(self):
        self.Server = config.Server
        self.force_apk = config.force_apk
        self.check_on_server()

    def check_on_server(self):
        url = self.Server + "Version2.json"
        r = requests.get(url)
        Ergebnis = r.json()
        self.Version = Ergebnis['BulkVersion']
        self.forced_pogo = Ergebnis['ForcedPogo']
        self.Support32 = Ergebnis['32bitSupport']
        self.Support64 = Ergebnis['64bitSupport']
        self.PogoDroid = Ergebnis['PogoDroid']
        print("Current Bulkupdate Version: "+str(self.Version))
        print("Forced Pogo: "+str(self.forced_pogo))
        print("32 bit Support: "+str(self.Support32))
        print("64 bit Support: "+str(self.Support64))
        print("Current PogoDroid Version: "+str(self.PogoDroid)+"\n")

    def download_pogo(self,bits,version):
        if version == "latest":
            self.download_pogo_latest(bits)
        elif version == "stable":
            self.download_pogo_stable(bits)

    def download_pogo_latest(self,bitversion):
        print("Start downloading .....")
        if self.force_apk == False:
            Name = self.Support64 + "_"+str(bitversion)+".apks"
            url = self.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.Support64 + "_"+str(bitversion)+".apk"
            url = self.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

        print("Downloaded new Version")

    def download_pogo_stable(self,bitversion):
        print("Start downloading .....")
        if self.force_apk == False:
            Name = self.forced_pogo + "_"+str(bitversion)+".apks"
            url = self.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.forced_pogo + "_"+str(bitversion)+".apk"
            url = self.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

        print("Downloaded new Version")

    def download_Pogodroid(self):
        print("Start downloading .....")
        url = config.Server+ "uploads/PogoDroid.apk"
        r = requests.get(url, allow_redirects=True)
        open("PogoDroid.apk", 'wb').write(r.content)

    def clear_folder(self):
        print("Start clearing your Folder .....")
        #dont_delete = config.ADB + config.This_Programm
        dont_delete = config.dont_delete
        files = glob.glob('*')
        for f in files:
            if f not in dont_delete:
                os.remove(f)
                #print(f)
                pass
        print("Folder cleared.")

if __name__ == "__main__":
    I = Downloader()
    #I.clear_folder()
    #I.download_pogo_latest("64")
    #I.clear_folder()
    #I.download_pogo_stable(64)
    I.clear_folder()