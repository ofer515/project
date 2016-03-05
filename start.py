from Tkinter import *
import win32com.shell.shell as shell
import os
import sys
import subprocess

process = {}
games = ["PapersPlease.exe"]
def main_window():
    main_window = Tk()
    main_window.geometry("500x500")
    main_window.iconbitmap(os.path.abspath(os.curdir+"\Assets\Alien_robot.ico"))#r"C:\Users\ofer\Desktop\github files\project\Alien_robot.ico")
    main_window.wm_title("Personal Helper!")
    l = Label(text="Personal helper!")
    b = Button(main_window, text="start scanning for programs", command=scan_computer_programs)
    l.pack()
    b.pack()
    main_window.mainloop()


def scan_computer_programs():
    privs = 'asadmin'
    filename = "Data/programs_finder.py"
    if sys.argv[-1] != privs:
        script = os.path.dirname(filename) + os.path.basename(filename)
        params = ' '.join([script] + sys.argv[1:] + [privs])
        try:
            print "made it"
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        except Exception as e:
            print e
            print "need admin"

def running_programs(main_window, working):  #working is that the user doesnt want games and such to be reachable
    cmd = 'WMIC PROCESS get Caption,Processid,Priority,workingsetsize'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print process.keys()
    for line in proc.stdout:
        proc_vals = str(line).split(" ")
        if proc_vals[0] not in process.keys():
            print proc_vals[0]
            process[proc_vals[0]] = proc_vals[1:]

    if working:
        for key in process.keys():
            #print 'Taskkill /IM ' + key + ' /F'
            if key in games:
                print "hi"
                cmd = 'Taskkill /IM ' + key + ' /F'
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                process.pop(key)

        


if __name__ == "__main__":
    main_window()