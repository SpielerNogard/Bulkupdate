import ast
import glob
import config
from Commander import Commander
class DeviceHandler(object):
    def __init__(self):
        self.get_all_devices()
        
        self.Commander = Commander()
        self.connect_all_devices()
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

    def connect_all_devices(self):
        for ip in self.ip_32:
            cmd = "adb connect "+str(ip)
            Ergebnis = self.Commander.use_system_command(cmd)
        
        for ip in self.ip_64:
            cmd = "adb connect "+str(ip)
            Ergebnis = self.Commander.use_system_command(cmd)

    def disconnect_all_devices(self):
        Ergebnis = self.Commander.use_system_command("adb disconnect")
        return(Ergebnis)

    def install_packages(self,ip):
        cmd = "adb -s "+ip+" install-multiple -r "+self.find_apks()
        #print(cmd)
        Ergebnis = self.Commander.use_system_command(cmd)
        return(Ergebnis)

    def uninstall_package(self,ip,packages):
        cmd = "adb -s "+ip+" uninstall "+str(packages)
        Ergebnis =self.Commander.use_system_command(cmd)
        return(Ergebnis)
    
    def find_apks(self):
        Files = glob.glob('*.apk')
        Befehl = ""
        Ausgabe = ""
        for a in Files:
            Befehl = Befehl + a + " "
        return(Befehl)

if __name__ == "__main__":
    I = DeviceHandler()
    I.connect_all_devices()
    I.disconnect_all_devices()