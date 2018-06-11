import piSSH

selfUser = piSSH.user()
selfUser.set(ip = '192.168.1.101')
client = piSSH.client()
client.set(ip = '192.168.1.102')
client.connecting(AutoAddPolicy = True)
client.getAllConnectedUsers(printInfo = True)
client.banUsers(banUsers = ['192.442.2.11','192.168.1.103'])
try:
    while True:
        pass
except:
    client.stopBanning()
    print('CTRL + C pressed')
   
#client.kickAllUsers(allowUsers = selfUser)
#client.shutdown()
