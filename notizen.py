    def check_status(self):
        done = True
        for ip in self.ip_32:
            if ip not in self.erledigt:
                done = False
            
        for ip in self.ip_64:
            if ip not in self.ip_64:
                done = False

        return(done)
        
    
        done = self.check_status()
        if done == True:
            self.erledigt = []
            self.write_done_device()
        else:
            print("Not all Devices succesfull")