import piSSH

selfUser = piSSH.user()
selfUser.set(ip = '192.168.1.104')
client = piSSH.client(ip = '192.168.1.101', password = 'eete')
client.connecting(AutoAddPolicy = True)
#client.command(command = 'pip3 install vk', inputting = 'y')
client.getAllConnectedUsers(printInfo = True)
client.allowUsers(['192.442.2.11',selfUser.get()[0]])

client.getFiles()
try:
    while True:
        pass
except:
    #client.shutdown()
    client.close()
    print('CTRL + C pressed')
   

