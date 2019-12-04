#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:19:56 2019

@author: markb
"""

import os
from pathlib import Path

class Config:
    def __init__(self):
        home = str(Path.home())
        self.configPath = home + "/.ssh_manager/config.conf"
        self.vals = {}
        self.fileExists = os.path.exists(self.configPath)
        
    def load(self):
        if os.path.exists(self.configPath):
            self.fileExists = True
            with open(self.configPath, ) as configFile:
                for line in configFile:
                    conf = list(line.split(sep=":"))
                    key = conf[0].strip()
                    val = conf[1].strip()
                    self.vals[key] = val
        else:
            self.fileExists = False
        
    def get(self, key):
        if key in self.vals.keys():
            return self.vals[key]
        return None
    
    def set(self, key, val):
        self.vals[key] = val
        
    def createFile(self):
        home = str(Path.home())
        try:
            os.mkdir(home + "/.ssh_manager")
        except(FileExistsError):
            pass
        file = open(self.configPath, "w+")
        for key in self.vals:
            file.write("{0}:{1}".format(key, self.vals[key]))
        file.close()
        
    