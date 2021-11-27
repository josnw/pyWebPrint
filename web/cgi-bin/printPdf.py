#!/usr/bin/env python3

import cgi
import cgitb
from pathlib import Path
import configparser
import requests
import uuid
import os
import platform

cgitb.enable()

def readConfig(typ):
    configParser = configparser.RawConfigParser()   
    configFilePath = Path("../pywebprint.conf")
    configParser.read(configFilePath)
    printer = configParser.get('printer', typ)
    return printer

def printHeader():
    print("Content-Type: text/html")
    print()
    return

def printFilePOSIX(filename, printer):
    cmd = "lpr -P '" + printer + "' '" + filename + "'"
    print(cmd)
    os.system(cmd)

def printFileWIN(filename, printer):
    import win32api
    import win32print
    from glob import glob

    defaultPrinter = win32print.GetDefaultPrinter()
    win32print.SetDefaultPrinter(printer)
    win32api.ShellExecute(0, "print", filename, None,  ".",  0)
    win32print.SetDefaultPrinter(defaultPrinter)

if __name__ == '__main__':
    printHeader()

    form = cgi.FieldStorage()
    if "pdfurl" not in form:
        print("<H1>Error</H1>")
        print("Please define PDF URL!")
    else:
        pdfFileName = str(Path("./label" + str(uuid.uuid4()) + ".pdf"))
        pdfData = requests.get(form["pdfurl"].value)
        with open(pdfFileName, 'wb') as f:
            f.write(pdfData.content)
        if platform.system() == 'Windows':
            printFileWIN(pdfFileName,readConfig('label'))
        else:
            printFilePOSIX(pdfFileName,readConfig('label'))
        os.remove(pdfFileName)

