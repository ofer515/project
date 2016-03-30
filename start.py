from Tkinter import *
from ttk import Frame, Button, Label, Style,Treeview,Scrollbar
import win32com.shell.shell as shell
import os
import sys
import subprocess
#from gi.repository import Gtk
import thread

import time
import tkMessageBox

threads = {"procs": "empty"}
process = {}
games = ["PapersPlease.exe", "Steam.exe"]

columns = ["Process Name",
           "Id",
           "Priority",
           "Usage"]


class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()


    def initUI(self):
        self.parent.title("Personal Helper")
        self.pack(fill=BOTH, expand=True)


        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)

        #area = Gtk.ListStore(str, str, str)
        area = Treeview(self)
        area['show'] = 'headings'
        area["columns"]= ("one", "two", "three", "four")
        area.column("one", width=10)
        area.column("two", width=10)
        area.column("three", width=10)
        area.column("four", width=10)
        area.heading("one", text="process name")
        area.heading("two", text="Priority")
        area.heading("three", text="PID")
        area.heading("four", text="Usage")


        area.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)

        abtn = Button(self, text="Activate", command=scan_computer_programs)
        abtn.grid(row=1, column=3)

        sbtn = Button(self, text="Stop", command=lambda: stop_running(area, threads["procs"]))
        sbtn.grid(row=2, column=3,pady=6)

        cbtn = Button(self, text="Close", command=quit)
        cbtn.grid(row=3, column=3, pady=4)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK", command=lambda: call_runnig(area, threads["procs"]))
        obtn.grid(row=5, column=3)



def main1():
    main_window = Tk()
    main_window.geometry("500x500")
    main_window.iconbitmap(os.path.abspath(os.curdir+"\Assets\Alien_robot.ico"))#r"C:\Users\ofer\Desktop\github files\project\Alien_robot.ico")
    main_window.wm_title("Personal Helper!")
    l = Label(text="Personal helper!")
    CheckVal1 = IntVar()
    w = Checkbutton(main_window, text = "work", variable = CheckVal1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
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
    root.iconbitmap(os.path.abspath(os.curdir+"\Assets\Alien_robot.ico"))
    app = Window(root)
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
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)

        except Exception as e:
            print e
            print "need admin"


def stop_running(area, threadP):
    if threads["procs"] is not "empty":
        threads["procs"].exit()
        threads["procs"] = "empty"


def call_runnig(area, thread1):
        if thread1 is not "empty":
            tkMessageBox.showinfo("Error", "already up")
        else:
            threads["procs"] = thread.start_new_thread(running_programs,(area, ))




def running_programs(area): # (add working):  #working is that the user doesnt want games and such to be reachable
    while True:
        cmd = 'WMIC PROCESS get Caption,Processid,Priority,workingsetsize'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            try:
                area.insert("", 0, text="line1", values=(line))
            except Exception as e:
                print e
                print line
                raw_input("stopped")
            proc_vals = str(line).split(" ")
            if proc_vals[0] not in process.keys():
                print proc_vals[0]
                process[proc_vals[0]] = proc_vals[1:]
        time.sleep(10)
        area.delete(*area.get_children())

"""
    if working:
        for key in process.keys():
            #print 'Taskkill /IM ' + key + ' /F'
            if key in games:
                print "hi", key
                cmd = 'Taskkill /IM ' + key + ' /F'
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                process.pop(key)

   """


if __name__ == "__main__":
    root = Tk()
    main()
