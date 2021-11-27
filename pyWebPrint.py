from tkinter import *
from tkinter.ttk import *
from pystray import MenuItem as item
import pystray
from pathlib import Path
import configparser
from PIL import Image
import os
import platform
import http.server
import socketserver
import cgitb
import threading




def quit_window(icon, item):
    icon.stop()
    httpd.shutdown()
    win.destroy()

def show_window(icon, item):
    icon.stop()
    win.after(0,win.deiconify())

def hide_window():
    win.withdraw()
    image=Image.open("../tray.ico")
    menu=(item('Beenden', quit_window), item('Konfiguration', show_window))
    icon=pystray.Icon("pyWebPrint", image, "pyWebPrint", menu)
    icon.run()

def getPrinter():
    if platform.system() == "Windows":
        all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        return all_printer
    else:
        return os.popen('lpstat -e').read().split("\n")
    
def saveConf():
    if not configParser.has_section('printer'):
        configParser.add_section('printer')
    configParser.set('printer', 'label', combo.get())
    fp=open('../pywebprint.conf','w')
    configParser.write(fp)
    hide_window()
    return 0

def readConfig(typ):
    configFilePath = Path("../pywebprint.conf")
    configParser.read(configFilePath)
    if configParser.has_option('printer', typ):
        printer = configParser.get('printer', typ)
        return printer
    else:
        return ""

def miniServer():
    httpd.serve_forever()   
    
    
if __name__ == "__main__":
    
    win=Tk()
    win.title("pyWebPrint")
    win.geometry("400x400")
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    os.chdir(web_dir)
    
    configParser = configparser.RawConfigParser()
    
    cgitb.enable()
    
    PORT = 8091
    HOST = "localhost"
    
    handler = http.server.CGIHTTPRequestHandler
    
    httpd = socketserver.TCPServer((HOST, PORT), handler)
    httpd.server_name = "pyWebPrint"
    httpd.server_port = PORT
    print("serving at host ", HOST, ":", PORT)
    
    
    
    serv = threading.Thread(target=miniServer, daemon=True)
    serv.start()
    
    lbl = Label(win, text="pyWebPrint Konfiguration", font=("Arial Bold", 15))
    lbl.grid(column=0, row=0, columnspan=2, sticky='W', padx= 10,pady= 20)
    lbl = Label(win, text="Wähle den Label Drucker")
    lbl.grid(column=0, row=1, columnspan=2, sticky='NW', padx= 10,pady= 20)
    
    
    lbl = Label(win, text="Label Printer:")
    lbl.grid(column=0, row=2, padx= 10,sticky='W')
    
    combo = Combobox(win)
    printerList = [ readConfig('label') ]
    printerList.extend(getPrinter())
    combo['values']= printerList
    combo.current(0)
    combo.grid(column=1, row=2, padx= 10,sticky='W')
    
    
    btnSave = Button(win, text="Speichern", command=saveConf)
    btnSave.grid(column=0, row=3,  columnspan=1, padx= 10, pady= 100, sticky='SE')
    btnClose = Button(win, text="Beenden", command=win.destroy)
    btnClose.grid(column=1, row=3,  columnspan=1, padx= 10, pady= 100, sticky='SE')
    
    
    win.protocol('WM_DELETE_WINDOW', hide_window)
    
    if readConfig('label') != "":
        hide_window()
    win.mainloop()
