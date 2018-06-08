import piSSH
client = piSSH.client()
client.set(ip = '')
client.connecting(AutoAddPolicy = True)
client.command(command = 'hostname -I', sudo = True)
client.shutdown()
