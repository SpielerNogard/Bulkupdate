import requests
import os
import zipfile
import glob
import subprocess
import ast
import time
import pyfiglet




class BulkUpdate(object):
    def __init__(self,auftrag):
        self.need_more = True
        self.Server = "http://157.90.184.181/"
        ascii_banner = pyfiglet.figlet_format("BulkUpdate")
        print(ascii_banner)
        
        if auftrag == "1":
            self.clear_Folder()
            self.start_updating()
        elif auftrag == "2":
            self.clear_Folder()
            self.download_pogodroid()
            self.update_droid()
        elif auftrag == "3":
            self.clear_Folder()
            self.download_rgc()
            self.update_rgc()
        elif auftrag == "4":
            Test = input("Which .apk you want to install ? (only the name without the .apk) ")
            self.install_any_apk(Test)
        else: 
            print("This is not a vaild id")

    def find_version(self):
        print("Searching for new Pogo Version ...")
        url = self.Server + "Version.json"
        r = requests.get(url)
        Ergebnis = r.json()
        self.Version = Ergebnis['Version']
        print("Found Version: "+str(self.Version))


    def download_newest_version(self):
        print("Start downloading .....")
        Name = self.Version + ".apks"
        url = self.Server + "uploads/"+Name
        r = requests.get(url, allow_redirects=True)
        open(Name, 'wb').write(r.content)
        print("Downloaded new Version")
        print("Start renaming into .zip......")
        os.rename(self.Version + '.apks', self.Version + '.zip')
        print("Renamed  into .zip")
        

    def unzip_files(self):
        print("start extracting files ....")
        zip = zipfile.ZipFile(self.Version + '.zip')
        zip.extractall()
        print("all files extracted")

    def get_all_apks(self):
        print("searching for .apk ....")
        self.Files = glob.glob('*.apk')
        self.Befehl = ""
        Ausgabe = ""
        for a in self.Files:
            self.Befehl = self.Befehl + " " + a
            Ausgabe = Ausgabe + ", "+a
        print("found the following files : "+str(Ausgabe))
   
    def clear_Folder(self):
        print("Start clearing your Folder .....")
        This_Programm = ['main.py','ips.txt','updated.txt','multi_at_once.py']
        ADB = ["adb.exe","AdbWinApi.dll","AdbWinUsbApi.dll","avcodec-58.dll","avformat-58.dll","avutil-56.dll","scrcpy.exe","scrcpy-noconsole.exe","scrcpy-server","SDL2.dll","swresample-3.dll","swscale-5.dll"]
        dont_delete = ADB + This_Programm
        files = glob.glob('*')
        for f in files:
            if f not in dont_delete:
                os.remove(f)

        print("Folder cleared.")
    
    def get_all_devices(self):
        print("Searching for devices .....")
        IP_Adressen = "ips.txt"
        erledigt = "updated.txt"
        alle_ips= open(IP_Adressen).read()
        bereits_erledigt = open(erledigt).read()
        self.alle_ips = ast.literal_eval(alle_ips)
        self.erledigt = ast.literal_eval(bereits_erledigt)
        Ausgabe = ""
        for a in self.alle_ips:
            Ausgabe = Ausgabe + ", "+a
        print("found the following devices : "+ str(Ausgabe))

    def connect_to_device(self,ip):
        print("connecting to: "+str(ip)+".......")
        subprocess.call("adb connect "+str(ip),shell=True)
        print("conected to: "+str(ip))

    def install_update(self, APK_Name):
        print("installing "+APK_Name+" .....")
        subprocess.call("adb install -r "+str(APK_Name)+".apk",shell=True)
        print(APK_Name+ " installed")

    def install_packages(self):
        print("installing packages ...")
        subprocess.call("adb install-multiple -r "+ self.Befehl,shell=True)
        print("all packages installed")

    def disconnect_device(self,ip):
        print("disconnecting from: "+str(ip)+".......")
        subprocess.call("adb disconnect "+str(ip),shell=True)
        print("disconnected from : "+str(ip))

    def start_updating(self):
        print("Start updating your Devices ......")
        self.find_version()
        self.download_newest_version()
        self.unzip_files()
        self.get_all_apks()
        self.get_all_devices()

        for a in self.alle_ips:
            if a in self.erledigt:
                print(str(a)+ " is already up to date skipping.....")
            
            else:
                if self.need_more == True:
                    self.connect_to_device(a)
                    self.install_packages()
                    self.disconnect_device(a)
                    self.erledige_device(a)
                    self.check_status()
            

        self.clear_Folder()
        print("Update finished")
    
    def erledige_device(self,ip):
        self.erledigt.append(ip)
        datei = open('updated.txt','w')
        datei.write(str(self.erledigt))

    def check_status(self):
        status = True
        for a in self.alle_ips:
            if a not in self.erledigt:
                status = False

        if status == True:
            print("Update finished ")
            test = []
            datei = open('updated.txt','w')
            datei.write(str(test))
            self.need_more = False

    def download_pogodroid(self):
        url = "https://www.maddev.eu/apk/PogoDroid.apk"
        print("Start downloading Pogodroid.....")
        r = requests.get(url, allow_redirects=True)
        open("PogoDroid.apk", 'wb').write(r.content)
        print("Downloaded new Version")

    def update_droid(self):
        print("Start updating your Devices ......")
        self.get_all_devices()

        for a in self.alle_ips:
            if a in self.erledigt:
                print(str(a)+ " is already up to date skipping.....")
            
            else:
                if self.need_more == True:
                    self.connect_to_device(a)
                    self.install_update("PogoDroid")
                    self.disconnect_device(a)
                    self.erledige_device(a)
                    self.check_status()

    def install_any_apk(self,APK):
        print("Start updating your Devices ......")
        self.get_all_devices()

        for a in self.alle_ips:
            self.connect_to_device(a)
            self.install_update(APK)
            self.disconnect_device(a)

    def download_rgc(self):
        url = "https://raw.githubusercontent.com/Map-A-Droid/MAD/master/APK/RemoteGpsController.apk"
        print("Start downloading RGC.....")
        r = requests.get(url, allow_redirects=True)
        open("RemoteGpsController.apk", 'wb').write(r.content)
        print("Downloaded new Version")
    
    def update_rgc(self):
        print("Start updating your Devices ......")
        self.get_all_devices()

        for a in self.alle_ips:
            if a in self.erledigt:
                print(str(a)+ " is already up to date skipping.....")
            
            else:
                if self.need_more == True:
                    self.connect_to_device(a)
                    self.install_update("RemoteGpsController")
                    self.disconnect_device(a)
        


print("this program supports the following functions")
print("1 : Autoupdate pogo on all your devices")
print("2 : Update Pogodroid on all your devices")
print("3 : Update RemoteGpsController on all your devices")
print("4 : install your own .apk on all your devices")

Test = input("Please enter the id of the order which is to be carried out ")
BulkUpdate = BulkUpdate(Test)



