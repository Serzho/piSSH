#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time

import piSSH

class BanningThread(threading.Thread):
    def __init__(self, name = '', pause = 0.5):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        self.pause = pause

    def setClient(self, client):
        self.client = client
        self.running = True
        
    def run(self):
        while self.running:
            try:
                self.client.getAllConnectedUsers()
                self.client.kickBannedUsers(self.name)
            except:
                pass
            time.sleep(self.pause)
        print('Thread %s stopped\n' % self.name)

    def stop(self):
        self.running = False
    
