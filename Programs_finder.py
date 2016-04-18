import StringIO
import traceback
import wmi
import sys
from _winreg import (HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, 
                     OpenKey, EnumValue, QueryValueEx)
import tkMessageBox


def main():
    new_file = open('programs_list.log', 'w')
    errorLog = open('errors.log', 'w')
    displies = open('displayList.log', 'w')
    r = wmi.Registry()
    result, names = r.EnumKey(hDefKey=HKEY_LOCAL_MACHINE, sSubKeyName=r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
    new_file.write('These subkeys are found under "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall"\n\n')
    errorLog.write("Errors\n\n")
    separator = "*" * 80
    keyPath = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    for subkey in names:
        try:
            new_file.write(separator + '\n\n')
            path = keyPath + "\\" + subkey
            key = OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_ALL_ACCESS)
            try:
                temp = QueryValueEx(key, 'DisplayName')
                display = str(temp[0])
                if display is not "":
                    new_file.write('Display Name: ' + display + '\nRegkey: ' + subkey + '\n')
                    displies.write(display+"\n")

                else:
                    pass
            except:
                new_file.write('Regkey: ' + subkey + '\n')

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
    new_file.close()
    errorLog.close()
    tkMessageBox.showinfo("Error", "Done scanning")

if __name__ == "__main__":
    main()
else:
    print __name__