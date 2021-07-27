import requests
import pyfiglet
import urllib
import ast
import os
import zipfile
import glob
import subprocess

import config

class Bulkupdate(object):
    def __init__(self):
        self.ip_32 = []
        self.ip_64 = []
        self.erledigt = []

        self.check_on_server()
        self.get_all_devices()
        self.bulkupdate()

    def check_on_server(self):
        url = config.Server + "Version2.json"
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

    def get_all_devices(self):
        alle_ips_32= open(config.IP_Adressen_32bit).read()
        alle_ips_64= open(config.IP_Adressen_64bit).read()
        bereits_erledigt = open(config.Erledigte_Devices).read()

        self.ip_32 = ast.literal_eval(alle_ips_32)
        self.ip_64 = ast.literal_eval(alle_ips_64)
        self.erledigt = ast.literal_eval(bereits_erledigt)
        print("Found "+str(len(self.ip_64) + len(self.ip_32))+" devices\n")

    def add_device_64(self):
        ip = input("Please enter your IP Adress 64bit: ")
        self.ip_64.append(ip)
        datei = open(config.IP_Adressen_64bit,'w')
        datei.write(str(self.ip_64))
        print("done CTRL+C to abort")
        datei.close()
        self.add_device_64()

    def add_device_32(self):
        ip = input("Please enter your IP Adress 32bit: ")
        self.ip_32.append(ip)
        datei = open(config.IP_Adressen_32bit,'w')
        datei.write(str(self.ip_32))
        print("done CTRL+C to abort")
        datei.close()
        self.add_device_32()

    def list_devices(self):
        for device in self.ip_32:
            print(device," 32bit")
        for device in self.ip_64:
            print(device," 64bit")
    
    def download_pogo_latest64(self):
        print("Start downloading .....")
        if config.force_apk == False:
            Name = self.Support64 + "_64.apks"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.Support64 + "_64.apk"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

        print("Downloaded new Version")
    
    def download_pogo_stable64(self):
        print("Start downloading .....")
        if config.force_apk == False:
            Name = self.forced_pogo + "_64.apks"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.forced_pogo + "_64.apk"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

        print("Downloaded new Version")

    def download_pogo_latest32(self):
        print("Start downloading .....")
        if config.force_apk == False:
            Name = self.Support32 + "_32.apks"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.Support32 + "_32.apk"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

        print("Downloaded new Version")

    def download_pogo_stable_32(self):
        print("Start downloading .....")
        if config.force_apk == False:
            Name = self.forced_pogo + "_32.apks"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)
            os.rename(Name,'Pogo.zip')
            zip = zipfile.ZipFile('Pogo.zip')
            zip.extractall()
        else:
            Name = self.forced_pogo + "_32.apk"
            url = config.Server+ "uploads/"+Name
            r = requests.get(url, allow_redirects=True)
            open(Name, 'wb').write(r.content)

    def download_Pogodroid(self):
        print("Start downloading .....")
        url = config.Server+ "uploads/PogoDroid.apk"
        r = requests.get(url, allow_redirects=True)
        open("PogoDroid.apk", 'wb').write(r.content)
        

    def clear_folder(self):
        print("Start clearing your Folder .....")
        dont_delete = config.ADB + config.This_Programm
        files = glob.glob('*')
        for f in files:
            if f not in dont_delete:
                os.remove(f)
        print("Folder cleared.")

    def connect_all_devices(self):
        for ip in self.ip_32:
            self.connect_to_device(ip)
        
        for ip in self.ip_64:
            self.connect_to_device(ip)
    
    def search_for_apk(self):
        print("searching for .apk ....")
        self.Files = glob.glob('*.apk')
        self.Befehl = ""
        Ausgabe = ""
        for a in self.Files:
            self.Befehl = self.Befehl + " " + a
            Ausgabe = Ausgabe + ", "+a
        print("found the following files : "+str(Ausgabe))

    def install_packages(self,ip):
        print("installing packages ...")
        #subprocess.call("adb uninstall com.nianticlabs.pokemongo",shell=True)
        subprocess.call("adb -s "+ip+" install-multiple -r "+ self.Befehl,shell=True)

    def uninstall_pogo(self,ip):
        print("uninstalling Pogo")
        subprocess.call("adb -s "+ip+" uninstall com.nianticlabs.pokemongo",shell=True)

    def erledige_device(self,ip):
        self.erledigt.append(ip)
        self.write_done_device()

    def write_done_device(self):
        datei = open(config.Erledigte_Devices,'w')
        datei.write(str(self.erledigt))
        datei.close()
    def check_status(self):
        done = True
        for ip in self.ip_32:
            if ip not in self.erledigt:
                done = False
            
        for ip in self.ip_64:
            if ip not in self.ip_64:
                done = False

        return(done)

    def pogo_stable(self):
        self.clear_folder()
        self.disconnect_all()
        self.connect_all_devices()

        if len(self.ip_32) > 0:
            self.download_pogo_stable_32()
            self.search_for_apk()
            for ip in self.ip_32:
                if ip not in self.erledigt:
                    #self.uninstall_pogo()
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
                    
            self.clear_folder()

        if len(self.ip_64) > 0:
            self.download_pogo_stable64()
            self.search_for_apk()
            for ip in self.ip_64:
                if ip not in self.erledigt:
                    #self.uninstall_pogo()
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.clear_folder()

        self.disconnect_all()

        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")

    def pogo_latest(self):
        self.clear_folder()
        self.disconnect_all()
        self.connect_all_devices()

        if len(self.ip_32) > 0:
            self.download_pogo_latest32()
            self.search_for_apk()
            for ip in self.ip_32:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
                    
            self.clear_folder()

        if len(self.ip_64) > 0:
            self.download_pogo_latest64()
            self.search_for_apk()
            for ip in self.ip_64:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.clear_folder()

        self.disconnect_all()

        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")
        

    def PogoDroid_update(self):
        self.clear_folder()
        self.disconnect_all()
        self.connect_all_devices()
        self.download_Pogodroid()
        self.search_for_apk()
        if len(self.ip_32) > 0:
            for ip in self.ip_32:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
                    
            self.clear_folder()

        if len(self.ip_64) > 0:
            for ip in self.ip_64:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.clear_folder()

        self.disconnect_all()

        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")
        
    def disconnect_all(self):
        subprocess.call("adb disconnect",shell=True)
        
    def connect_to_device(self,ip):
        subprocess.call("adb connect "+str(ip),shell=True)

    def install_both(self):
        self.clear_folder()
        self.disconnect_all()
        self.connect_all_devices()

        self.download_Pogodroid()
        if len(self.ip_32) > 0:
            self.download_pogo_latest32()
            self.search_for_apk()
            for ip in self.ip_32:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
                    
            self.clear_folder()

        if len(self.ip_64) > 0:
            self.download_pogo_latest64()
            self.search_for_apk()
            for ip in self.ip_64:
                if ip not in self.erledigt:
                    #self.install_packages(ip)
                    self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.clear_folder()

        self.disconnect_all()

        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")

    def bulkupdate(self):
        print("Welcome at Bulkupdate")
        print("this program supports the following functions\n")
        print("1: List your devices")
        print("2: add IP Adresses to your list (64bit)")
        print("3: add IP Adresses to your list (32bit)")
        print("4: Start POGO Update to latest supported Version")
        print("5: Start POGO Update to latest stable Version (downgrade) This will uninstall Pogo first")
        print("6: Start PogoDroid Update")
        print("7: Update POGO and PogoDroid")
        print("\n")
        Test = input("Please enter the id of the order which is to be carried out ")

        if Test == "1":
            self.list_devices()
        elif Test == "2":
            self.add_device_64()
        elif Test == "3":
            self.add_device_32()
        elif Test == "4":
            self.pogo_latest()
        elif Test == "5":
            self.pogo_stable()
        elif Test == "6":
            self.PogoDroid_update()
        elif Test == "7":
            self.install_both()

if __name__ == "__main__":
    I = Bulkupdate()