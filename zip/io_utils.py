#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester

Utilities to open, edit, and write, save files
"""
import pandas as pd

# open a file, return its contents
# param inputFile the path to the file to be opened (relative or absolute path ok)
def get_file_contents(inputFile):
    input_file = open(inputFile, 'r', encoding='utf-8', errors='igonre')
    contents = input_file.read()
    return contents

# write text out to specified file
# param text is a STRING to write out
# param outputFile the path to the output (relative or absolute path, must include extension)
def writer(text, outputFile):
    output_file = open(outputFile, "w+")
    output_file.write(text)
    output_file.close()

# copy template file and replace the contents to generate a new filled in file
# param templateFile the file to open and generate a new filed based off of
# param outputFile the destination file for the edited/filled in template file, including extension
# textToReplace a string or ORDERED list of strings of things to replace
# replacements the text to take the place of textToReplace, a string or ORDERED list of strings (in order ot textToReplace)
def fill_template(templateFile, outputFile, textToReplace, replacements):
    template_contents = get_file_contents(templateFile)
    edited_contents = ""
    if type(textToReplace) == str:
        edited_contents = template_contents.replace(textToReplace, str(replacements))
    elif type(textToReplace) == list:
        edited_contents = template_contents
        for i in range(0, len(textToReplace)):
            edited_contents = edited_contents.replace(textToReplace[i], str(replacements[i]))
    writer(edited_contents, outputFile)

# read in parameters stored in and provided via an excel or csv file
# param inputFile the input excel or csv file
# paam sheetName optional sheet name to check if using excel file
# return params a dictionary of parameters
def read_params(inputFile, sheetName=False):
    if inputFile.endswith(".csv"):
        df = pd.read_csv(inputFile)
    elif inputFile.endswith(".xlsx"):
        if sheetName:
            df = pd.read_excel(inputFile, sheet=sheetName)
        else:
            df = pd.read_excel(inputFile)
    return params

# save parameters from GUI to csv or excel file
#def save_params():