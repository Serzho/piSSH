import paramiko
import piSSH

class user():
    def __init__(self, information = ''):
        try:
            info = information.split()
            self.ip = info[2]
            self.number = info[1][4]
            self.loginTime = (int((str(info[3][0])) + (str(info[3][1])) ), int((str(info[3][3])) + (str(info[3][4]))))
        except:
            self.ip = '127.0.0.1'
            self.number = '-1'
            self.loginTime = (0,0)

    def set(self, ip = '127.0.0.1', number = '-1', loginTime = (0,0)):
        if(ip != self.ip):
            self.ip = ip
        if(number != self.number):
            self.number = number
        if(loginTime != self.loginTime):
            self.loginTime = loginTime

    def get(self):
        return (self.ip, self.number, self.loginTime)
