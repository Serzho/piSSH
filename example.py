import piSSH

selfUser = piSSH.user()
selfUser.set(ip = '192.168.1.104')
client = piSSH.client(ip = '192.168.1.101')
client.findPassword()
client.connecting(AutoAddPolicy = True)
client.command(command = 'pip3 install vk', inputting = 'y')
client.getAllConnectedUsers(printInfo = True)
client.banUsers(banUsers = ['192.442.2.11','192.168.1.103'])
client.downloadFile('example.py','ex.py')
try:
    while True:
        pass
except:
    client.close()
    print('CTRL + C pressed')
   
#client.kickAllUsers(allowUsers = selfUser)
#client.shutdown()
