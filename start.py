from Tkinter import *
from ttk import Frame, Button, Label, Style, Treeview, Scrollbar, Checkbutton
import win32com.shell.shell as shell
import os
import sys
import subprocess
#from gi.repository import Gtk
import thread
import win32api, win32process, win32con
import time
import tkMessageBox

threads = {"procs": "empty"}
process = {}
working_bans = ["PapersPlease.exe", "Steam.exe", "chrome.exe"]
system_process =["pythonw.exe", "dllhost.exe", "cmd.exe", "WMIC.exe"]
run_cond = True
columns = ["Process Name",
           "Id",
           "Priority",
           "Usage"]

#standart window for my program
class Window(Frame):
    def __init__(self, parent, window_type):
        Frame.__init__(self, parent, msg = None)

        self.parent = parent
        if window_type == "main":
            self.initUI_main()
        if window_type == "err":
            self.initUI_err()

    def initUI_main(self):
        self.parent.title("Personal Helper")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)
        self.rowconfigure(6, pad=6)

        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)

        check_val = IntVar()
        check1 = Checkbutton(self, text="work?(will defuse some processes)", variable=check_val)
        check1.grid(row=6, column=0)


        #area = Gtk.ListStore(str, str, str)
        area = Treeview(self)
        area['show'] = 'headings'
        area["columns"] = ("one", "two", "three", "four")
        area.column("one", width=10)
        area.column("two", width=10)
        area.column("three", width=10)
        area.column("four", width=10)
        area.heading("one", text="process name")
        area.heading("two", text="Priority")
        area.heading("three", text="PID")
        area.heading("four", text="Usage")

        area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E + W + S + N)

        abtn = Button(self, text="Activate", command=scan_computer_programs)
        abtn.grid(row=1, column=3)

        sbtn = Button(self, text="Stop", command=lambda: stop_running(area, threads["procs"]))
        sbtn.grid(row=2, column=3, pady=6)

        cbtn = Button(self, text="Close", command=quit)
        cbtn.grid(row=3, column=3, pady=4)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK", command=lambda: call_running(area, threads["procs"],check_val))

        obtn.grid(row=5, column=3)

    def initUI_err(self):
        self.parent.title("Personal Helper")
        self.pack(fill=BOTH, expand=True)



#older version,  might prove useful in the future so I wont remove it yet
def main1():
    main_window = Tk()
    main_window.geometry("500x500")
    main_window.iconbitmap(os.path.abspath(
        os.curdir + "\Assets\Alien_robot.ico"))  #r"C:\Users\ofer\Desktop\github files\project\Alien_robot.ico")
    main_window.wm_title("Personal Helper!")
    l = Label(text="Personal helper!")
    CheckVal1 = IntVar()
    w = Checkbutton(main_window, text="work", variable=CheckVal1, \
                    onvalue=1, offvalue=0, height=5, \
                    width=20)
    b = Button(main_window, text="start scanning for programs", command=scan_computer_programs)
    #c = Button(main_window, text="block all gaming apps", command=running_programs(main_window,True))
    l.pack()
    b.pack()
    c.pack()
    w.pack()
    print CheckVal1
    main_window.mainloop()



def main():
    root.geometry("450x400+300+300")
    root.iconbitmap(os.path.abspath(os.curdir + "\Assets\Alien_robot.ico"))
    app = Window(root, "main")
    root.mainloop()


def scan_computer_programs():
    privs = 'asadmin'
    filename = "Programs_finder.py"
    print filename
    if sys.argv[-1] != privs:
        print sys.argv[0]
        script = os.path.dirname(filename) + os.path.basename(filename)
        params = ' '.join([script] + sys.argv[1:] + [privs])
        print params
        try:
            print "made it"
            print script
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)

        except Exception as e:
            print e
            tkMessageBox.showerror("Error", "Need to be admin")
            print "need admin"


def stop_running(area, threadP):
    global run_cond
    run_cond = False
    threads["procs"] = "empty"


def call_running(area, thread1,check_val):
    if thread1 is not "empty":
        tkMessageBox.showinfo("Error", "already up")
    else:
        threads["procs"] = thread.start_new_thread(running_programs, (area, check_val))

#doing what task manager is doing' showing realtime processes
def running_programs(area, check):  # (add working):  #working is that the user doesnt want games and such to be reachable
    global run_cond
    run_cond = True
    while run_cond:
        tag = ""
        cmd = 'WMIC PROCESS get Caption,Processid,Priority,workingsetsize'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            try:
                proc_vals = str(line).split(" ")
                if proc_vals[0] in system_process:
                    tag = "sys"
                if line != "":
                    area.insert("", 0, None, values=(line), tags = (tag,))
            except Exception as e:
                print e

                raw_input("stopped")
            #proc_vals = str(line).split(" ")
            if proc_vals[0] not in process.keys():
                print proc_vals[0]
                process[proc_vals[0]] = proc_vals[1:]
            area.tag_configure('sys', background='light blue')

        area.delete(*area.get_children())

        #checking if working status is on and defusing processes if necessary
        if check.get() == 1:
            for key in process.keys():
                #print 'Taskkill /IM ' + key + ' /F'
                if key in working_bans:
                    print "killing ", key
                    cmd = 'Taskkill /IM ' + key + ' /F'
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    process.pop(key)
        time.sleep(20)
#in dev - must choose how to use
def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])


if __name__ == "__main__":
    root = Tk()
    main()
