import piSSH
client = piSSH.client()
client.set(ip = '192.168.1.101')
client.connecting(AutoAddPolicy = True)
client.command(command = 'hostname -I', sudo = True)
client.getAllConnectedUsers()
#client.shutdown()
