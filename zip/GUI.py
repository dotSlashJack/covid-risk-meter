#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester

Generate a GUI to accept user parameters, routines to run, etc.
"""
import tkinter as tk
from tkinter import filedialog

"""
Build a GUI
param windowName, a string, the title for the window
param dims, a list, the dimensions (in pixels) of the GUI window to create as [width, height]
"""
class GUI:
    def __init__(self,windowName="COVID Metric GUI",dims=[500,700]):
       root = tk.Tk()
       self.root = root
       self.windowName = windowName
       self.dims = dims
    
    # add a label to the GUI
    # param text the text of the label
    # param pack whether or not to automatically pack/display the label
    # return label the label object in the GUI
    # return label_text, the text (as a string) of the label created
    def add_label(self, text, pack=False):
        label_text = tk.StringVar()
        label_text.set(text)
        #label = tk.Label(text=text)
        label = tk.Label(self.root, textvariable=label_text)
        if pack:
            label.pack()
        return label, label_text
    
    # update a label's text (assumes it was already packed)
    # param lab the label to update
    # param new_text the new label text to update to
    def update_label(self, lab, new_text):
        lab.set(new_text)

    # add a button to the GUI
    # param buttonText the text to be displayed on the button
    # param command, the command to run when the button is clicked
    # param pack, whether or not to automatically pack/display the button
    # param pack_pos, a tkinter position argument to tell the button where to be packed
    # return button, the button object added to the GUI
    def add_button(self, buttonText, command, dims=False, pack=False, pack_pos=False):
        if dims:
            button = tk.Button(
                text=buttonText,
                width=dims[0],
                height=dims[1],
                command = command
            )
        else:
            button = tk.Button(text=buttonText, command=command)
        if pack:
            if pack_pos:
                button.pack(side=pack_pos)
            else:
                button.pack()
        return button

    # param text the text label for the checkbox
    # param var the variable it'll update
    # param pack whether or not to pack/display the checkbox
    # return checkbox, the checkbox object that was created
    def add_checkbox(self, text, var, pack=False):
        checkbox = tk.Checkbutton(self.root, text = text, variable = var, onvalue = 1, offvalue = 0)
        if pack:
            checkbox.pack()
        return checkbox

    # get the status of a provided checkbox (useful if you need to return the int value)
    # param box the checkbox object to get the status of
    # return box.get(), the checkbox value (ideally an integer 0 or 1)
    def get_checkbox_status(self, box):
        return box.get()

    # create a file selection dialogue to ask user to select a file
    # param text_field the tkinter label of the text field that will show the user which file was selected
    # param init_dir the ddefault directory users are in when they begin file selection process
    # param file_types a tuple containing n tuples, where each tuple has the file type description and the extension as its elements
    # return filename, the name (path) of the file selected by the user
    def add_file_dialogue(self, text_field, init_dir="/", file_types=(("excel files","*.xlsx"),("all files","*.*"))):
        filename = filedialog.askopenfilename(initialdir = init_dir, title = "Select file", filetypes = file_types )
        self.update_label(text_field, filename)
        return filename
    
    # closes the window provided at init
    def close_window(self):
        self.root.destroy()
    
    # pack (display) provided tkinter object
    # param tkObject the thing you want to pack
    # WARNING: this is deprecated and will be removed in future versions
    def pack(self, tkObject):
        tkObject.pack()

    # builds the GUI (call after all labels, checkboxes, buttons, etc. have been configured)
    def build_gui(self):
        self.root.title(self.windowName)
        self.root.minsize(self.dims[0],self.dims[1])
        self.root.mainloop()