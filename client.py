#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import BanningThread as BanThr
import copy as c
import subprocess as sp
import time


import piSSH
import user as u

class user(u.user):
    pass

class bthr(BanThr.BanningThread):
    pass

class client(paramiko.SSHClient):
    def __init__(self, mode = 'public', password = 'raspberry' , tracking = False,
                   port = '22', ip = '127.0.0.1', name = 'pi', printInfo = True):
        paramiko.SSHClient.__init__(self)
        self.password = password
        self.port = port
        self.ip = ip
        self.name = name
        pI = printInfo
        self.__updateStatus('Setted', printInfo)
        self._users = []
        self.__mode = mode
        self.tracking = tracking
        self.log('STARTED %s' % time.asctime(time.localtime(time.time())))

    def __updateStatus(self, status, printInfo = True):
        self._status = status
        if(printInfo):
            print(self._status)      

    def log(self, string):
        if(self.tracking):
            f = open('logs/clientLog%s' % self.ip,'a')
            f.write(string + '\n')
            f.close()

    def getMode(self):
        return self.__mode
    
    def connecting(self, AutoAddPolicy = False, password = '', returnInfo = False, printInfo = True):
        if(password != ''):
            self.password = password
        if(self.name == 'pi' and self.password == 'raspberry'):
            if(printInfo):
                print("Connecting with default parameters...")
        else:
            if(printInfo):
                print("Connecting with given parameters...")
        if(AutoAddPolicy):
            if(printInfo):
                print('Auto add in known_hosts!')
            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if(printInfo):
                print('Connecting...')
            self.connect(self.ip, username = self.name, password = self.password,\
                         port = self.port)
            if(returnInfo):
                return True
            if(printInfo):
                print('Success!!!')
            self.sftp = self.open_sftp()
            self.__updateStatus('Connected')
        except:
            if(returnInfo):
                return False
            if(printInfo):
                print('Connection error!!!')
        self.ban()

    def command(self, sudo = False, returnInfo = True, command = '', printInfo = True, inputting = ''):
        if(sudo):
            command = "sudo " + command
        try:
            if(printInfo):
                print("Trying to: %s" % command)
            stdin, stdout, stderr = self.exec_command(command)
            if(sudo):
                stdin.write(self.password + '\n')
                stdin.flush()
            if(type(inputting) == 'list'):
                for line in inputting:
                    stdin.write(line + '\n')
                    stdin.flush()
            else:
                if(inputting != ''):
                    stdin.write(inputting + '\n')
                    stdin.flush()
            if(printInfo):
                print("RETURN: ")
                for line in stdout.readlines():
                    print(line)
            if(returnInfo):
                return stdout.readlines()
        except:
            if(returnInfo):
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
                self._users.clear()
            if(printInfo):
                print('Getting all connected users...')
            info = self.command(sudo = False, returnInfo = True, printInfo = False, command = 'w')
            if(len(info)>2):
                for i in range(len(info)-2):
                    self._users.append(user(info[i+2]))
                if(printInfo):
                    for u in self._users:
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
        
    def kickBannedUsers(self):
        f = open("known_users/denyUsers%s" % self.ip,'r')
        denyUsers = f.readlines()
        for line in denyUsers:
            for u in self._users:
                if (str(line).split() == u.get()[0].split()):
                    self.kick(u)
        f.close()
        
    def kickUnknownUsers(self):
        f = open("known_users/allowUsers%s" % self.ip,'r')
        allowUsers = f.readlines()
        known = False
        for u in self._users:
            for line in allowUsers:
                if (str(line).split() == u.get()[0].split()):
                    known = True
                    self.log(line)
                self.log(str(u.get()[0].split()))
            if(not known):
                self.kick(u)
            else:
                known = False
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
        self.__mode = 'public'
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
                print(banUsers)
                f.write('%s\n' % banUsers)
            else:
                for line in info.split():
                    if(line == banUsers):
                        already = True
                if(not already):
                    print(banUsers)
                    f.write('%s\n' % banUsers)
                else:
                    print('Already banned: %s' % banUsers)
        f.close()
        self.ban()

    def allowUsers(self, allowUsers):
        self.__mode = 'private'
        already = False
        try:
            f = open("known_users/allowUsers%s" % self.ip,'r')
            info = f.read()
            f.close()
        except:
            print('no already allowed users at this client')
            info = '0.0.0.0'
        print('Add to banned list: ')
        f = open("known_users/allowUsers%s" % self.ip,'a')
        if(type(allowUsers) != 'str'):
            for bU in allowUsers:
                for line in info.split():
                    if(bU == line):
                        print('Already allowed: %s' % bU)
                        already = True
                if(not already):
                    f.write('%s\n' % bU)
                else:
                    already = False
        else:
            if(info == '0.0.0.0'):
                print(allowUsers)
                f.write('%s\n' % allowUsers)
            else:
                for line in info.split():
                    if(line == allowUsers):
                        already = True
                if(not already):
                    print(allowUsers)
                    f.write('%s\n' % allowUsers)
                else:
                    print('Already allowed: %s' % allowUsers)
        f.close()
        self.ban()

    def findPassword(self, threads = 3):
        info = sp.check_output('python3 password.py %d %s %s %s' % \
                                        (threads, self.ip, self.name, self.port), shell = True)
        out = ''
        for line in info:
            out += chr(line)
        print(out)
        try:
            f = open('temp.txt', 'r')
            self.password = f.read()
            f.close()
        except:
            print('No password fined')
    def __format(self, s = ''):
        S = s.split('/')
        s = ''
        S.remove('home')
        S.remove(self.name)
        S.pop(0)
        for i in range(len(S)):
            if(i == 0):
                s += S[i]
            else:
                s += '/' + S[i]
        return s
        
    def downloadFile(self, originalName = '', finalName = '', isTree = False):
        if(self._status == 'Connected'):
            print(originalName)
            if(isTree):
                finalName = 'download/%s' % finalName.split('/')[len(finalName.split('/')) - 1]
            else:
                finalName = 'download/%s' % finalName
            originalName = self.__format(originalName)
            finalName = 'download/%s' % originalName
            print(originalName)
            try:
                try:
                    self.sftp.get(originalName, finalName)
                    print('%s saved as %s' % (originalName.split()[0], finalName))
                except:
                    sp.call('mkdir -p ~/piSSH/%s' % finalName, shell = True)
                    self.sftp.get(originalName.split()[0], finalName)
            except:
                print('Error downloading file')
        else:
            return False
            print('No connection to server!!!')

    def uploadFile(self, originalName = '', finalName = ''):
        if(self._status == 'Connected'):
            self.sftp.put(originalName, finalName)
            print('%s uploaded as %s' % (originalName, finalName))
            print('Error upload file...')
        else:
            print('No connection to server!!!')

    def findFile(self, name = '', expansion = '.', printInfo = True):
        self.command(returnInfo = False, printInfo = False, command = 'apt install locale', sudo = True)
        self.command(returnInfo = False, printInfo = False, command = 'updatedb', sudo = True)
        if(name != ''):
            files = self.command(returnInfo = True, printInfo = False, command = 'locate %s%s'\
                         % (name, expansion), sudo = True)
        try:
            if(type(files) == 'str'):
                if(printInfo):
                    if(files != 'None'):
                        print('File was founded')
                        print(files)
                    else:
                        print('File not found')        
            else:
                if(printInfo):
                    print('A lot of files founded')
                    for file in files:
                        print(file)
            return files
        except:
            print('Error finding files...')

    def getFiles(self):
        self.command(returnInfo = False, printInfo = False, command = 'apt install locale', sudo = True)
        self.command(returnInfo = False, printInfo = False, command = 'updatedb', sudo = True)
        files = self.command(returnInfo = True, printInfo = False, command = "find ~ \( ! -regex '%s' \) -type f" % '.*/\..*' )
        for file in files:
            self.downloadFile(originalName = file, finalName = self.__format(file), isTree = True)
        

    def close(self):
        self.sftp.close()
        self.stopBanning()
