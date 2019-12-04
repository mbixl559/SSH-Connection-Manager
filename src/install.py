#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:27:44 2019

@author: markb
"""

import os
from pathlib import Path
import shutil

try:
    import tkinter
except ImportError:
    print("This requires the python tkinter module")
    print("please install tkinter by running:\n sudo apt-get update && sudo apt-get install python3-tk")
    exit()

def runInstall():
    home = str(Path.home())
    currDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(currDir)
    libDir = os.path.join(home, ".local", "lib")
    #print(libDir)
    #print(os.path.sys.path)
    for d in os.path.sys.path:
        if libDir in d:
            libDir = d
            break
        
    print("Copying required packages...")
    srcLib = os.path.join(currDir, "app", "sshmanager")
    destLib = os.path.join(libDir, "sshmanager")
    if os.path.exists(destLib):
        shutil.rmtree(destLib)
    shutil.copytree(srcLib, destLib)
    
    print("Copying runable...")
    srcProg = os.path.join(currDir, "app", "ssh-manager.py")
    destProg = os.path.join(libDir, "ssh-manager.py")
    if os.path.exists(destProg):
        os.remove(destProg)
    shutil.copyfile(srcProg, destProg)
    
    print("Creating symlink...")
    symLink = "/usr/local/bin/ssh-manager"
    if os.path.exists(symLink):
        os.remove(symLink)
    os.symlink(destProg, symLink)
    add_execute(symLink)
    
    print("Done!")
    
    
def add_execute(path): # https://stackoverflow.com/a/30463972
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

if __name__ == "__main__":
    runInstall()