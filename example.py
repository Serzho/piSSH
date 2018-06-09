import piSSH
selfUser = piSSH.user()
selfUser.set(ip = '')
client = piSSH.client()
client.set(ip = '')
client.connecting(AutoAddPolicy = True)
client.getAllConnectedUsers(printInfo = True)
client.kickAllUsers(allowUsers = selfUser)
#client.shutdown()
