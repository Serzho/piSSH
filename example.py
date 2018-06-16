import piSSH

selfUser = piSSH.user()
selfUser.set(ip = '')
client = piSSH.client(ip = '', password = '')
client.connecting(AutoAddPolicy = True)
client.command(command = 'ls', printInfo = True)
client.getAllConnectedUsers(printInfo = True)
client.allowUsers(['',selfUser.get()[0]])
client.getFiles()

try:
    while True:
        pass
except:
    client.close()
    client.shutdown()
    print('CTRL + C pressed')
   

