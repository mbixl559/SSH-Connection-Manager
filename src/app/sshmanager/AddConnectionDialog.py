#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:03:03 2019

@author: markb
"""

import os
import tkinter as tk

class AddConnectionDialog:
    def __init__(self, master):
        self.master = master
        self.root = None
        self.serverTitle = tk.StringVar()
        self.server = tk.StringVar()
        self.user = tk.StringVar()
        self.keyfile = tk.StringVar()
        self.submitListener = None
        
    def show(self):
        self.root = tk.Toplevel(self.master)
        self.__buildUI()
        
    def __buildUI(self):
        wrapper = tk.Frame(self.root, padx=8, pady=8)
        wrapper.pack()
        
        title = tk.Label(wrapper, text="Add Connection", font="Helvetica 18 bold")
        title.pack(anchor=tk.CENTER)
        
        titleInputFrame = tk.Frame(wrapper,padx=2, pady=2)
        titleInputFrame.pack(fill=tk.X)
        serverTitleLabel = tk.Label(titleInputFrame, text="Connection Title")
        serverTitleLabel.pack(anchor=tk.W)
        self.txtServerTitle = tk.Entry(titleInputFrame, textvariable=self.serverTitle)
        self.txtServerTitle.pack(anchor=tk.W)
        
        serverInputFrame = tk.Frame(wrapper, padx=2, pady=2)
        serverInputFrame.pack(fill=tk.X)
        serverLabel = tk.Label(serverInputFrame, text="Server Name")
        serverLabel.pack(anchor=tk.W)
        self.txtServer = tk.Entry(serverInputFrame, textvariable=self.server)
        self.txtServer.pack(anchor=tk.W)
        
        userInputFrame = tk.Frame(wrapper, padx=2, pady=2)
        userInputFrame.pack(fill=tk.X)
        userLabel = tk.Label(userInputFrame, text="User")
        userLabel.pack(anchor=tk.W)
        self.txtUser = tk.Entry(userInputFrame, textvariable=self.user)
        self.txtUser.pack(anchor=tk.W)
        
        keyfileInputFrame = tk.Frame(wrapper, padx=2, pady=2)
        keyfileInputFrame.pack(fill=tk.X)
        keyfileLabel = tk.Label(keyfileInputFrame, text="Public Key")
        keyfileLabel.pack(anchor=tk.W)
        keyfileInputWrapper = tk.Frame(keyfileInputFrame)
        keyfileInputWrapper.pack(anchor=tk.W)
        self.txtKeyFile = tk.Entry(keyfileInputWrapper, textvariable=self.keyfile)
        self.txtKeyFile.pack(side=tk.LEFT)
        btnSelectKeyfile = tk.Button(keyfileInputWrapper, text="Open", command=self.__selectKeyFile)
        btnSelectKeyfile.pack(side=tk.RIGHT)
        
        footerFrame = tk.Frame(wrapper)
        footerFrame.pack(fill=tk.X, pady=5)
        actionButtonsFrame = tk.Frame(footerFrame)
        actionButtonsFrame.pack(side=tk.RIGHT)
        
        btnOK = tk.Button(actionButtonsFrame, text="OK", command=self.__submit)
        btnOK.pack(side=tk.LEFT)
        
        btnCancel = tk.Button(actionButtonsFrame, text="Cancel", command=self.quit)
        btnCancel.pack(side=tk.RIGHT)
    
    def __submit(self):
        title = self.serverTitle.get()
        server = self.server.get()
        user = self.user.get()
        keyfile = self.keyfile.get()
        
        if title is None or title == "":
            tk.messagebox.showerror("Error", "Server Title is required")
            return
            
        if server is None or server == "":
            tk.messagebox.showerror("Error", "Server name is required")
            return
            
        if user is None or user == "":
            tk.messagebox.showerror("Error", "User is required")
            return
        
        if self.submitListener is not None:
            self.submitListener(title, server, user, keyfile)
        self.quit()
    
    def __selectKeyFile(self):
        file = tk.filedialog.askopenfilename(parent=self.root, title="Select public key file:")
        self.keyfile.set(file)
        self.txtKeyFile.delete(0, tk.END)
        self.txtKeyFile.insert(0, file)
    
    def setSubmitListener(self, listener):
        self.submitListener = listener
    
    def quit(self):
        self.root.destroy()