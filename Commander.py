import subprocess

class Commander(object):
    def __init__(self):
        pass

    def use_system_command(self,cmd):
        erwarteter_return = []
        if "connect" in cmd:
            erwarteter_return = ["connected to","already connected to"]
        if "disconnect" in cmd:
            erwarteter_return = ["disconnected","disconnected everything"]
        if "install-multiple" in cmd:
            erwarteter_return = ["Success"]
        
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        
        if self.check_returns(stdout,erwarteter_return) == True:
            #print("Success")
            return(True)
        
        else:
            #print("Fehler")
            return(False)
        
    def check_returns(self,got_return,erwarteter_return):
        success = False

        stdout1 = got_return.splitlines()
        for line in stdout1:
            print(line.decode("UTF-8"))

        for möglicher_return in erwarteter_return:
            if möglicher_return.encode("UTF-8") in got_return:
                success = True
        
        return(success)