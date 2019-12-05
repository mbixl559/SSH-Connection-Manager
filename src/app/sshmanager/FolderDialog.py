#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:36:37 2019

@author: markb
"""

import os
import tkinter as tk

class FolderDialog:
    def __init__(self, master):
        self.master = master
        self.initDir = os.getcwd()
        self.folder = tk.StringVar()
        self.folder.set(self.initDir)
        
        self.finishListener = None
        
        
        
    def show(self):
        self.root = tk.Toplevel(self.master)
        self.root.title("Add Connection")
        self.__buildUI()
        
    def __buildUI(self):
        inputFrame = tk.Frame(self.root, padx=8)
        inputFrame.pack()
        
        self.txtFolder = tk.Entry(inputFrame, textvariable=self.folder)
        self.txtFolder.pack(side=tk.LEFT)
        
        btnSelectFolder = tk.Button(inputFrame, text="Select Folder", command=self.__showFolderSelect)
        btnSelectFolder.pack(side=tk.RIGHT)
        
        controlsFrame = tk.Frame(self.root)
        controlsFrame.pack()
        btnOk = tk.Button(controlsFrame, text="OK", command=self.__done)
        btnOk.pack()
        
    def __showFolderSelect(self):
        folder = tk.filedialog.askdirectory(parent=self.root, initialdir=self.initDir, title="Select folder: ")
        self.setValue(folder)
        
    def __done(self):
        if self.folder.get() == "":
            tk.messagebox.showerror("Error", "Project folder cannot be empty")
        else:
            self.root.destroy()
            if self.finishListener is not None:
               self.finishListener() 
    
    def getValue(self):
        return self.folder.get()
    
    def setValue(self, val):
        self.folder.set(val)
        self.txtFolder.delete(0, tk.END)
        self.txtFolder.insert(0, val)
    
    def setFinishListener(self, listener):
        self.finishListener = listener