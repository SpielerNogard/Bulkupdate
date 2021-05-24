import multiprocessing as mp
import ast
import time
import pyfiglet
import requests
import os
import zipfile
import glob
import subprocess

class BulkUpdate():
    def __init__(self,auftrag):
        self.Server = "http://157.90.184.181/"
        ascii_banner = pyfiglet.figlet_format("BulkUpdate")
        print(ascii_banner)

        self.clear_Folder()
        if auftrag == "1":
            self.find_version()
            self.download_newest_version()
            self.unzip_files()
        elif auftrag == "2":
            self.download_pogodroid()
        else: 
            self.Ausgabe("This is not a valid ID")
        self.get_all_devices()

    def Ausgabe(self,Nachricht):
        print("[BulkUpdate]: "+Nachricht+"\n")

    def download_pogodroid(self):
        url = "https://www.maddev.eu/apk/PogoDroid.apk"
        self.Ausgabe("Start Donwloading PogoDroid")
        r = requests.get(url, allow_redirects=True)
        open("PogoDroid.apk", 'wb').write(r.content)
        self.Ausgabe("Downloaded Pogodroid")

    def get_all_devices(self):
        self.Ausgabe("Searching for Devices")
        IP_Adressen = "ips.txt"
        erledigt = "updated.txt"
        alle_ips= open(IP_Adressen).read()
        bereits_erledigt = open(erledigt).read()
        self.alle_ips = ast.literal_eval(alle_ips)
        self.erledigt = ast.literal_eval(bereits_erledigt)
        Ausgabe = ""
        for a in self.alle_ips:
            Ausgabe = Ausgabe + ", "+a
            self.Ausgabe("Found following device: "+str(a))

    def find_version(self):
        self.Ausgabe("Searching for new PoGo Version")
        url = self.Server + "Version.json"
        r = requests.get(url)
        Ergebnis = r.json()
        self.Version = Ergebnis['Version']
        self.Ausgabe("Found Version: "+str(self.Version))
    
    def download_newest_version(self):
        self.Ausgabe("Start Donwloading .....")
        Name = self.Version + ".apks"
        url = self.Server + "uploads/"+Name
        r = requests.get(url, allow_redirects=True)
        open(Name, 'wb').write(r.content)
        self.Ausgabe("Downloaded newest Version")
        self.Ausgabe("Start renaming into .zip")
        os.rename(self.Version + '.apks', self.Version + '.zip')
        self.Ausgabe("Renamed into .zip")

    def unzip_files(self):
        self.Ausgabe("Start extracting files")
        zip = zipfile.ZipFile(self.Version + '.zip')
        zip.extractall()
        self.Ausgabe("all Files extracted")

    def clear_Folder(self):
        self.Ausgabe("Start clearing your Folder")
        This_Programm = ['main.py','ips.txt','updated.txt','multi_at_once.py']
        ADB = ["adb.exe","AdbWinApi.dll","AdbWinUsbApi.dll","avcodec-58.dll","avformat-58.dll","avutil-56.dll","scrcpy.exe","scrcpy-noconsole.exe","scrcpy-server","SDL2.dll","swresample-3.dll","swscale-5.dll"]
        dont_delete = ADB + This_Programm
        files = glob.glob('*')
        for f in files:
            if f not in dont_delete:
                os.remove(f)

        self.Ausgabe("Folder cleared")


def Ausgaben(ip,Nachricht):
    print("["+ip+"]: "+Nachricht+"\n")

def connect_to_device(ip):
    Ausgaben(ip,"Connecting to Device")
    subprocess.call("adb connect "+str(ip),shell=True)
    Ausgaben(ip,"Connected")

def get_all_apks():
    Files = glob.glob('*.apk')
    Befehl = ""
    for a in Files:
        Befehl = Befehl + " " + a
    return(Befehl)

def install_update(APK_Name, ip):
    Ausgaben(ip,"installing "+APK_Name)
    subprocess.call("adb -s "+ip+" install-multiple -r "+str(APK_Name),shell=True)
    print(APK_Name+ " on "+ip+" installed")
    Ausgaben(ip,APK_Name+" installed")

def disconnect_device(ip):
    Ausgaben(ip,"disconnecting ....")
    subprocess.call("adb disconnect "+str(ip),shell=True)
    Ausgaben(ip,"disconnected")

def my_func(ip):
    alle_apks = get_all_apks()
    connect_to_device(ip)
    install_update(alle_apks,ip)
    disconnect_device(ip)
    #print(ip)

def main(auftrag):
    BOB = BulkUpdate(auftrag)
    alle_ips = BOB.alle_ips
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(my_func, alle_ips)
    BOB.clear_Folder()

if __name__ == "__main__":
    print("this program supports the following functions")
    print("1 : Autoupdate pogo on all your devices")
    print("2 : Update Pogodroid on all your devices")


    Test = input("Please enter the id of the order which is to be carried out ")
    main(Test)