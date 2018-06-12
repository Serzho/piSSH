#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import BanningThread as BanThr
import copy as c

import piSSH
import user as u

class user(u.user):
    pass

class bthr(BanThr.BanningThread):
    pass

class client(paramiko.SSHClient):
    def __init__(self, password = 'raspberry' , port = '22', ip = '127.0.0.1', name = 'pi'):
        paramiko.SSHClient.__init__(self)
        self.password = password
        self.port = port
        self.ip = ip
        self.name = name
        self.__updateStatus('Setted')
        self._users = []

    def __updateStatus(self, status):
        self._status = status
        print(self._status)      
    
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
            self.connect(self.ip, username = self.name, password = self.password,\
                         port = self.port)
            print('Success!!!')
            self.__updateStatus('Connected')
        except:
            print('Connection error!!!')
        self.ban()

    def command(self, sudo = False, returnInfo = True, command = '', printInfo = True):
        if(sudo):
            command = "sudo " + command
        try:
            if(printInfo):
                print("Trying to: %s" % command)
            stdin, stdout, stderr = self.exec_command(command)
            if(sudo):
                stdin.write(self.password + '\n')
                stdin.flush()
            if(printInfo):
                print("RETURN: ")
                for line in stdout.readlines():
                    print(line)
            if(returnInfo):
                return stdout.readlines()
        except:
            print('Command error!!!')

    def reboot(self):
        self.__updateStatus('Disconnected')
        print('Rebooting....')
        self.command(sudo = True, returnInfo = False, command = 'reboot now')
        

    def shutdown(self):
        self.__updateStatus('Disconnected')
        print('Shutdowning...')
        self.command(sudo = True, returnInfo = False, command = 'shutdown now')
    
    def getAllConnectedUsers(self, printInfo = False):
        if(self._status=='Connected'):
            if(len(self._users) != 0):
                self.users.clear()
            if(printInfo):
                print('Getting all connected users...')
            info = self.command(sudo = False, returnInfo = True, printInfo = False, command = 'w')
            if(len(info)>2):
                for i in range(len(info)-2):
                    self.users.append(user(info[i+2]))
                if(printInfo):
                    for u in self.users:
                        print()
                        print('///////////////')
                        print('User IP: %s' % u.get()[0])
                        print('User Number: %s' % u.get()[1])
                        print('Time connection: %d:%d' % u.get()[2])
                        print('///////////////')
                        print()
            else:
                if(printInfo):
                    print('No one connected user!!!')
        else:
            if(printInfo):
                print('Error: Not connected to server!!!')

    def kick(self, u):
        self.command(returnInfo = False, printInfo = False, \
                                command = ('skill -KILL -t pts/' + u.get()[1]))
        print('User IP: %s was kicked!!!' % u.get()[0])

    def ban(self):
        self._bthr = BanThr.BanningThread(name = self.ip, pause = 1)
        self._bthr.setClient(c.copy(self))
        self._bthr.start()

    def stopBanning(self):
        self._bthr.stop()
        self._bthr.join()
        
    def kickBannedUsers(self,ip):
        f = open("known_users/denyUsers%s" % self.ip,'r')
        denyUsers = f.readlines()
        for line in denyUsers:
            for u in self.users:
                if (str(line).split() == u.get()[0].split()):
                    self.kick(u)
        f.close()
    
    def kickAllUsers(self, allowUsers = u.user()):
        for u in self.users:
            if(type(allowUsers)=='list'):
                for aU in allowUsers:
                    if(u.ip != aU.ip):
                        self.kick(aU)
            else:
                if(allowUsers.ip != u.ip):
                    self.kick(u)
    
    def banUsers(self, banUsers):
        already = False
        try:
            f = open("known_users/denyUsers%s" % self.ip,'r')
            info = f.read()
            f.close()
        except:
            print('no already banned users at this client')
            info = '0.0.0.0'
        print('Add to banned list: ')
        f = open("known_users/denyUsers%s" % self.ip,'a')
        if(type(banUsers) != 'str'):
            for bU in banUsers:
                for line in info.split():
                    if(bU == line):
                        print('Already banned: %s' % bU)
                        already = True
                if(not already):
                    f.write('%s\n' % bU)
                else:
                    already = False
        else:
            if(info == '0.0.0.0'):
                print('ityity')
                print(banUsers)
                f.write('%s\n' % banUsers)
            else:
                for line in info.split():
                    if(line == banUsers):
                        already = True
                if(not already):
                    print('mmnmm')
                    print(banUsers)
                    f.write('%s\n' % banUsers)
                else:
                    print('Already banned: %s' % banUsers)
        f.close()
        self.ban()

        
