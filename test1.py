

import os
import sys
import win32com.shell.shell as shell
import tkMessageBox


privs = 'asadmin'
#filename = "Data\pf.py"
filename = "pf.py"
print filename
if sys.argv[-1] != privs:
    print sys.argv[0]
    print os.path.dirname(filename), "123"
    print os.path.basename(filename), "345"
    script = os.path.dirname(filename) + os.path.basename(filename)
    params = ' '.join([script] + sys.argv[1:] + [privs])
    print params

    print "made it"
    print script
    tkMessageBox.showinfo("made it")
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
