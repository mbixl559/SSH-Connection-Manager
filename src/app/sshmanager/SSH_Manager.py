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
from sshmanager.AddConnectionDialog import AddConnectionDialog

import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
from tkinter import Label
from tkinter import simpledialog

class SSH_Manager:
    def __init__(self):
        self.config = Config()
        self.clients = []
        self.projectFolder = os.getcwd()
        
        self.selectedClient = None
        
    def start(self):
        self.config.load()
            
        self.buildUI()
        self.run()
    
    def buildUI(self):
        self.uiRoot = Tk()
        self.uiRoot.title("SSH Connection Manager")
        self.uiRoot.minsize(80, 100)
        
        self.clientLabels = []
        self.serverLabels = []
        
        actionFrame = tk.Frame(self.uiRoot)
        actionFrame.pack(side=tk.TOP, fill=tk.X)
        
        self.btnAddClient = tk.Button(actionFrame, text="Add Client", command=self.handleAddClientClicked)
        self.btnAddClient.pack(side=tk.LEFT)
        
        self.btnAddConn = tk.Button(actionFrame, text="Add Connection", state=tk.DISABLED, command=self.handleAddConnClicked)
        self.btnAddConn.pack(side=tk.RIGHT)
        
        self.folderDialog = FolderDialog(self.uiRoot)
        self.folderDialog.setFinishListener(self.folderPicked)
        
        
        self.clientFrame = tk.Frame(self.uiRoot)
        self.clientFrame.pack(side=tk.LEFT, fill=tk.X)
        
        clientTitle = Label(self.clientFrame, text="Clients", font="Helvetica 18 bold")
        clientTitle.pack(anchor=tk.CENTER)
        
        self.serverFrame = tk.Frame(self.uiRoot)
        self.serverFrame.pack(side=tk.RIGHT, fill=tk.Y)
        
        
        if not self.config.fileExists:
            self.folderDialog.show()
            return
            
        self.buildClientList()
        
    def handleAddClientClicked(self):
        clientName = simpledialog.askstring("Create Client", "Client Name(no spaces):", parent=self.uiRoot)
        self.addClient(clientName)
        self.buildClientList()
        
    def handleAddConnClicked(self):
        dialog = AddConnectionDialog(self.uiRoot)
        dialog.setSubmitListener(self.addConnSubmitListener)
        dialog.show()   
    
    def addConnSubmitListener(self, title, server, user, keyfile):
        self.addClientServer(title, server, user, keyfile)
    
    def folderPicked(self):
        self.finishUI()
    
    def finishUI(self):
        projectDir = self.folderDialog.getValue()
        self.config.set("ssh-path", projectDir)
        self.config.createFile()
        self.buildClientList()
    
    def clearClientList(self):
        for label in self.clientLabels:
            label.destroy()
        self.clientLabels.clear()
        self.clients.clear()
        
    def addClient(self, clientName):
        if clientName is None:
            return
        projectPath = self.config.get("ssh-path")
        os.mkdir(os.path.join(projectPath, "clients", clientName))
    
    def buildClientList(self):
        self.clearClientList()
        self.load()
        
        for client in self.clients:
            w = Label(self.clientFrame, text=client, padx=10, pady=8)
            w.bind("<Button-1>", lambda e, client=client:self.lableClicked(client))
            w.pack(anchor=tk.CENTER)
            self.clientLabels.append(w)
    
    
    def showFolderDialog(self):
        answer = filedialog.askdirectory(parent=self.uiRoot, initialdir=os.getcwd(), title="Select SSH project folder: ")
        return answer
    
    def lableClicked(self, client):
        self.clearServers()
        self.loadClientServers(client)
        self.selectedClient = client
        self.btnAddConn.config(state=tk.NORMAL)
        
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
        self.clearServers()
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
    
    def clearServers(self):
        self.serverFrame.destroy()
        self.serverFrame = tk.Frame(self.uiRoot)
        self.serverFrame.pack(side=tk.RIGHT, fill=tk.Y)
    
    def addClientServer(self, title, server, user, keyfile):
        client = self.selectedClient
        
        projectPath = self.config.get("ssh-path")
        newConnFilePath = os.path.join(projectPath, "clients", client, title)
        
        contents = []
        contents.append("#! /bin/bash")
        contents.append("\n\n")
        
        
        keypart = "-i {}".format(keyfile) if keyfile is not None and keyfile != "" else ""
        serverpart = "@".join([user, server])
        
        sshCommand = " ".join(["ssh", keypart, serverpart])
        contents.append(sshCommand)           
        
        with open(newConnFilePath, "w+") as connFile:
            for line in contents:
                connFile.write(line)
        
        self.add_execute(newConnFilePath)
        
        self.loadClientServers(client)                  
        
            
    def serverClicked(self, client, server):
        projectPath = self.config.get("ssh-path")
        sshConnect = projectPath + "/" + "ssh_connect"
        
        subprocess.call(['gnome-terminal', '--', sshConnect, client, server])
        
    def add_execute(self, path): # https://stackoverflow.com/a/30463972
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2    # copy R bits to X
        os.chmod(path, mode)    
        