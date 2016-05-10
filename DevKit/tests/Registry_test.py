

import StringIO
import traceback
import wmi
import sys
from _winreg import (HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS,
                     OpenKey, EnumValue, QueryValueEx)
import tkMessageBox





r = wmi.Registry()
result, names = r.EnumKey(hDefKey=HKEY_LOCAL_MACHINE, sSubKeyName=r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
#new_file.write('These subkeys are found under "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall"\n\n')
#errorLog.write("Errors\n\n")
separator = "*" * 80
keyPath = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
for subkey in names:
    try:
        #new_file.write(separator + '\n\n')
        path = keyPath + "\\" + subkey
        key = OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_ALL_ACCESS)
        try:
            temp = QueryValueEx(key,)
            print str(temp)
            display = str(temp[0])
        except:
            pass
    except:
        pass