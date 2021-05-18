import threading
import time
import subprocess
import glob
import ast
import pyfiglet

# thread class to run a command
class ExampleThread(threading.Thread):
    def __init__(self, ip, apks, Device_Handler):
        threading.Thread.__init__(self)
        self.ip = ip
        self.apks = apks
        self.finished = False
        self.Device_Handler = Device_Handler

    def run(self):
        # execute the command, queue the result
        self.connect_to_device()
        self.get_all_apks()
        self.install_update()

    def connect_to_device(self):
        print("connecting to: "+str(self.ip)+".......")
        subprocess.call("adb connect "+str(self.ip),shell=True)
        print("conected to: "+str(self.ip))

    def get_all_apks(self):
        print("searching for .apk ....")
        self.Files = glob.glob('*.apk')
        self.Befehl = ""
        Ausgabe = ""
        for a in self.Files:
            self.Befehl = self.Befehl + " " + a
            Ausgabe = Ausgabe + ", "+a
        print("found the following files : "+str(Ausgabe))

    def install_update(self):
        self.get_all_apks()
        print("installing "+self.Befehl+" .....")
        subprocess.call("adb install -r "+str(self.Befehl)+".apk",shell=True)
        print(self.Befehl+ " installed")

    def device_done(self):
        self.Device_Handler.device_done(self.ip)

    
class Device_Handler():
    def __init__(self):
        self.get_all_devices()

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

    def device_done(self,ip):
        self.erledigt.append(ip)
        datei = open('updated.txt','w')
        datei.write(str(self.erledigt))


class BulkUpdate():
    def __init__(self):
        self.DeviceHandler = Device_Handler()
        self.Server = "http://157.90.184.181/"
        self.run()

    def run(self):
        ascii_banner = pyfiglet.figlet_format("BulkUpdate")
        print(ascii_banner)
        print("this program supports the following functions")
        print("1 : Autoupdate pogo on all your devices")
        print("2 : Update Pogodroid on all your devices")
        print("3 : Update RemoteGpsController on all your devices")
        auftrag = input("Please enter the id of the order which is to be carried out ")
        if auftrag == "1":
            print("Updating Pogo")
        elif auftrag == "2":
            print("Updating Pogodroid")
        elif auftrag == "3":
            print("Updating RGC")
        else: 
            print("This is not a vaild id")

    def clear_Folder(self):
        print("Start clearing your Folder .....")
        This_Programm = ['main.py','ips.txt','updated.txt']
        ADB = ["adb.exe","AdbWinApi.dll","AdbWinUsbApi.dll","avcodec-58.dll","avformat-58.dll","avutil-56.dll","scrcpy.exe","scrcpy-noconsole.exe","scrcpy-server","SDL2.dll","swresample-3.dll","swscale-5.dll"]
        dont_delete = ADB + This_Programm
        files = glob.glob('*')
        for f in files:
            if f not in dont_delete:
                os.remove(f)

        print("Folder cleared.")
        


ANU = BulkUpdate()

# define the commands to be run in parallel, run them
