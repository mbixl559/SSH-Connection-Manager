#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:43:04 2019

@author: markb
"""

import os
import subprocess

from sshmanager.config import Config
from sshmanager.FolderDialog import FolderDialog

import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
from tkinter import Label

class SSH_Manager:
    def __init__(self):
        self.config = Config()
        self.clients = []
        self.projectFolder = os.getcwd()
        
    def start(self):
        self.config.load()
            
        self.buildUI()
        self.run()
    
    def buildUI(self):
        self.uiRoot = Tk()
        self.uiRoot.minsize(80, 100)
        
        self.folderDialog = FolderDialog(self.uiRoot)
        self.folderDialog.setFinishListener(self.folderPicked)
        
        self.serverFrame = tk.Frame(self.uiRoot)
        self.serverFrame.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not self.config.fileExists:
            self.folderDialog.show()
            return
            
        self.buildClientList()
    
    def folderPicked(self):
        self.finishUI()
    
    def finishUI(self):
        projectDir = self.folderDialog.getValue()
        self.config.set("ssh-path", projectDir)
        self.config.createFile()
        
        self.buildClientList()
    
    def buildClientList(self):
        self.load()
        clientFrame = tk.Frame(self.uiRoot)
        clientFrame.pack(side=tk.LEFT)
        
        title = Label(clientFrame, text="Clients", font="Helvetica 18 bold")
        title.pack()
        
        for client in self.clients:
            w = Label(clientFrame, text=client, padx=10, pady=8)
            w.bind("<Button-1>", lambda e, client=client:self.lableClicked(client))
            w.pack()
    
    
    def showFolderDialog(self):
        answer = filedialog.askdirectory(parent=self.uiRoot, initialdir=os.getcwd(), title="Select SSH project folder: ")
        return answer
    
    def lableClicked(self, client):
        self.serverFrame.destroy()
        self.serverFrame = tk.Frame(self.uiRoot)
        self.serverFrame.pack(side=tk.RIGHT, fill=tk.Y)
        self.loadClientServers(client)
        
    def run(self):
        self.uiRoot.mainloop()
    
    def load(self):
        self.loadClients()
        os.chdir(self.config.get("ssh-path"))
        
    def loadClients(self):
        projectPath = self.config.get("ssh-path")
        if projectPath is None:
            exit()
        clientDir = projectPath + "/clients"
        if not os.path.exists(clientDir):
            os.mkdir(clientDir)
        self.clientDir = clientDir
        lst = os.listdir(clientDir)
        for i in lst:
            if os.path.isdir(clientDir + "/" + i):
                self.clients.append(i) 
                
    def loadClientServers(self, client):
        servers = []
        lst = os.listdir(self.clientDir + "/" + client)
        for server in lst:
            if len(server.split(".")) == 1 and not os.path.isdir("/".join([self.clientDir, client, server])):
                servers.append(server)
        
        title = Label(self.serverFrame, text="Servers", font="Helvetica 18 bold")
        title.pack()
        
        for server in servers:
            s = Label(self.serverFrame, text=server, padx=10, pady=8)
            s.bind("<Button-1>", lambda e, server=server:self.serverClicked(client, server))
            s.pack()
            
    def serverClicked(self, client, server):
        projectPath = self.config.get("ssh-path")
        sshConnect = projectPath + "/" + "ssh_connect"
        
        subprocess.call(['gnome-terminal', '--', sshConnect, client, server])
        
        
        