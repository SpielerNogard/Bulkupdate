#Update Server
Server = "http://62.68.75.189/"

#Do not use App Bundles to install your Updates ( False for APP Bundles, True for APK only)
force_apk = False

#The Files which holds your Ip Adresses
IP_Adressen_32bit = "IP32.txt"
IP_Adressen_64bit = "IP64.txt"
Erledigte_Devices = "updated.txt"


This_Programm = ['updated.txt','IP32.txt','IP64.txt','Version.json','Updater.py','BulkUpdate.py','config.py','README.md','requirements.txt','__pycache__',"Downloader.py","Commander.py","DeviceHandler.py","notizen.py"]
ADB = ["adb.exe","AdbWinApi.dll","AdbWinUsbApi.dll","avcodec-58.dll","avformat-58.dll","avutil-56.dll","scrcpy.exe","scrcpy-noconsole.exe","scrcpy-server","SDL2.dll","swresample-3.dll","swscale-5.dll"]
       
dont_delete = ADB+This_Programm

