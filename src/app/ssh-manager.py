#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:35:56 2019

@author: markb
"""

import os

from sshmanager import SSH_Manager

def main():
    pid = os.fork()
    if pid == 0:
        app = SSH_Manager()
        app.start() 

if __name__ == "__main__":
    main()