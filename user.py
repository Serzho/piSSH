import paramiko
import piSSH

class user():
    def __init__(self, information = ''):
        info = information.split()
        self.ip = info[2]
        self.number = info[1][4]
        self.loginTime = (int((str(info[3][0])) + (str(info[3][1])) ), int((str(info[3][3])) + (str(info[3][4]))))
        
    def get(self):
        return (self.ip, self.number, self.loginTime)
