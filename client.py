import paramiko
import piSSH

class client(paramiko.SSHClient):
    password = ''
    port = ''
    ip = ''
    name = ''
    status = 'none'

    def updateStatus(self, status):
        self.status = status
        print(self.status)

    def set(self, password = 'raspberry' , port = '22', ip = '127.0.0.1', name = 'pi'):
        self.password = password
        self.port = port
        self.ip = ip
        self.name = name
        self.updateStatus('Setted')
    
    def connecting(self, AutoAddPolicy = False):
        if(self.name == 'pi' and self.password == 'raspberry'):
            print("Connecting with default parameters...")
        else:
            print("Connecting with given parameters...")
        if(AutoAddPolicy):
            print('Auto add in known_hosts!')
            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print('Connecting...')
            self.connect(self.ip, username = self.name, password = self.password, port = self.port)
            print('Success!!!')
            self.updateStatus('Connected')
        except:
            print('Connection error!!!')

    def command(self, sudo = False, returnInfo = True, command = ''):
        if(sudo):
            command = "sudo " + command
        try:
            print("Trying to: %s" % command)
            stdin, stdout, stderr = self.exec_command(command)
            if(sudo):
                stdin.write(self.password + '\n')
                stdin.flush()
            if(returnInfo):
                print("RETURN: ")
                for line in stdout.readlines():
                    print(line)
        except:
            print('Command error!!!')

    def reboot(self):
        self.updateStatus('Disconnected')
        print('Rebooting....')
        self.command(sudo = True, returnInfo = False, command = 'reboot now')
        

    def shutdown(self):
        self.updateStatus('Disconnected')
        print('Shutdowning...')
        self.command(sudo = True, returnInfo = False, command = 'shutdown now')
    
    def getAllConnectedUsers(self):
        print('Getting all connected users...')
        self.command(sudo = False, returnInfo = True, command = 'w')
        
