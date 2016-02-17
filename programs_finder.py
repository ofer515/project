import StringIO
import traceback
import wmi
import win32com.shell.shell as shell
import sys
import os

from _winreg import (HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, 
                     OpenKey, EnumValue, QueryValueEx)

""""
privs = 'asadmin'
print sys.argv[0]
if sys.argv[-1] != privs:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [privs])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
"""



prog_list = open('programs_list.log', 'w')
errorLog = open('errors.log', 'w')


r = wmi.Registry()
result, names = r.EnumKey(hDefKey=HKEY_LOCAL_MACHINE, sSubKeyName=r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
 
prog_list.write('These subkeys are found under "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall"\n\n')
errorLog.write("Errors\n\n")
separator = "*" * 80
keyPath = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
for subkey in names:
    try:
        prog_list.write(separator + '\n\n')
        path = keyPath + "\\" + subkey
        key = OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_ALL_ACCESS) 
        try:
            temp = QueryValueEx(key, 'DisplayName')
            display = str(temp[0])
            if display is not "":
                prog_list.write('Display Name: ' + display + '\nRegkey: ' + subkey + '\n')
            else:
                pass
        except:
            prog_list.write('Regkey: ' + subkey + '\n')
 
    except Exception as e:
        print e
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        errorMessage = fp.getvalue()
        try:
            error = 'Error for ' + key + '. Message follows:\n' + errorMessage
            errorLog.write(error)
            errorLog.write("\n\n")
        except:
            pass
print "All programs that was needed are found"
print len(names)
prog_list.close()
errorLog.close()