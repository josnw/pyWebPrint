#!/usr/bin/env python3
import os
import platform

if platform.system() == "Windows":
    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    print(all_printer);
else:
    os.system('lpstat -e')
