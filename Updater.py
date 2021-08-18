import ast
import config
from Downloader import Downloader
from DeviceHandler import DeviceHandler
class Bulkupdate(object):
    def __init__(self):
        self.erledigt = []
        bereits_erledigt = open(config.Erledigte_Devices).read()
        self.erledigt = ast.literal_eval(bereits_erledigt)
        self.Downlader = Downloader()
        self.Devicehandler = DeviceHandler()

        self.version_to_install = "latest"
    
        self.bulkupdate()

    def erledige_device(self,ip):
        self.erledigt.append(ip)
        self.write_done_device()

    def write_done_device(self):
        datei = open(config.Erledigte_Devices,'w')
        datei.write(str(self.erledigt))
        datei.close()

    def check_status(self):
        done = True
        for ip in self.Devicehandler.ip_32:
            if ip not in self.erledigt:
                done = False
            
        for ip in self.Devicehandler.ip_64:
            if ip not in self.erledigt:
                done = False

        return(done)

    def pogo_update(self):
        self.Downlader.clear_folder()
        if len(self.Devicehandler.ip_32) > 0:
            self.Downlader.download_pogo(32,self.version_to_install)
            for ip in self.Devicehandler.ip_32:
                if ip not in self.erledigt:
                    if self.version_to_install == "stable":
                        self.Devicehandler.uninstall_package(ip,"com.nianticlabs.pokemongo")
                    ergebnis = self.Devicehandler.install_packages(ip)
                    if ergebnis == True:
                        self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
                    
            self.Downlader.clear_folder()

        if len(self.Devicehandler.ip_64) > 0:
            self.Downlader.download_pogo(64,self.version_to_install)
            for ip in self.Devicehandler.ip_64:
                if ip not in self.erledigt:
                    if self.version_to_install == "stable":
                        self.Devicehandler.uninstall_package(ip,"com.nianticlabs.pokemongo")
                    ergebnis = self.Devicehandler.install_packages(ip)
                    if ergebnis == True:
                        self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.Downlader.clear_folder() 

        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")

    def PogoDroid_update(self):
        self.Downlader.clear_folder()
        self.Downlader.download_Pogodroid()
        if len(self.Devicehandler.ip_32) > 0:
            for ip in self.Devicehandler.ip_32:
                if ip not in self.erledigt:
                    ergebnis = self.Devicehandler.install_packages(ip)
                    if ergebnis == True:
                        self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.Downlader.clear_folder()
        if len(self.Devicehandler.ip_64) > 0:
            for ip in self.Devicehandler.ip_64:
                if ip not in self.erledigt:
                    ergebnis = self.Devicehandler.install_packages(ip)
                    if ergebnis == True:
                        self.erledige_device(ip)
                else:
                    print(ip," already done skipping")
            self.Downlader.clear_folder()
        
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
        print("\n")
        Test = input("Please enter the id of the order which is to be carried out ")

        if Test == "1":
            self.Devicehandler.list_devices()
        elif Test == "2":
            self.Devicehandler.add_device_64()
        elif Test == "3":
            self.Devicehandler.add_device_32()
        elif Test == "4":
            self.version_to_install = "latest"
            self.pogo_update()
        elif Test == "5":
            self.version_to_install = "stable"
            self.pogo_update()
        elif Test == "6":
            self.PogoDroid_update()

if __name__ == "__main__":
    I = Bulkupdate()
    #I.clear_folder()
    #I.test_cmds("adb disconnect")
    #I.expand_path()
    #I.test_cmds("adb disconnect")