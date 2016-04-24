
from Tkinter import *
from ttk import Frame, Button, Label, Treeview, Checkbutton, Combobox, Entry
import win32com.shell.shell as shell
import os
import sys
import subprocess
import thread
import win32api, win32process, win32con
import time
import tkMessageBox
import webbrowser
import psutil
import pyautogui



threads = {"procs": "empty"}
process = {}
defults = {"block": "enter to block",
           "boost": "enter to buff priority",
           "degrade": "enter to lower priority",
           "music": "enter song's name"}
working_bans = ["PapersPlease.exe", "Steam.exe", "chrome.exe"]
blocks = open("Data\\blocked.log", 'r')
working_bans = blocks.read().splitlines()
blocks.close()
system_process =["pythonw.exe", "dllhost.exe", "cmd.exe", "WMIC.exe"]
boosted = open("Data\\boosted.log", 'r').read().splitlines()
degraded = open("Data\\degraded.log", 'r').read().splitlines()
music_list = {}
music_file = open("Data\\music_dic.log")
for line in music_file:
    name, url = line.split(":",1)
    music_list[name] = url[:-2]
music_file.close()
print type(music_list)
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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(5, pad=10)
        self.columnconfigure(3, pad=10)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(5, pad=7)
        self.rowconfigure(6, pad=6)


        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W+N, pady=4, padx=5)


        check_box = {"work": IntVar(),
                     "boost": IntVar()}

        check1 = Checkbutton(self, text="work-Mode", variable=check_box["work"])
        check1.grid(row=7, column=0)

        check2 = Checkbutton(self, text="boost games", variable=check_box["boost"])
        check2.grid(row=7, column=1)


        ### still not sure
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
        ###about this part
        #area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E + W + S + N)

        #comboboxes and relevent buttons

        self.block_drop = Combobox(self, postcommand= self.update_blocked)
        self.block_drop['values'] = working_bans
        self.block_drop.current(0)
        self.block_drop.grid(row=1, column=1, pady=1)
        self.entry = Entry(self)
        self.entry.insert(0, "enter to block")
        self.entry.grid(row=1, column=4)

        block_btn_remv = Button(self, text="Remove", command=lambda: remove_from_list(working_bans, self.block_drop.get()))
        block_btn_remv.grid(row=1, column=2)

        block_btn_add = Button(self, text="Add", command=lambda: add_to_list(working_bans, self.entry.get(), self.entry, defults["block"]))
        block_btn_add.grid(row=1, column=3)

        ############
        #boosted combo
        self.boost_drop = Combobox(self, postcommand=self.update_boosted)
        self.boost_drop['values'] = boosted
        self.boost_drop.current(0)
        self.boost_drop.grid(row=2, column=1, pady=1)
        self.entry2 = Entry(self)
        self.entry2.insert(0, "enter to buff priority")
        self.entry2.grid(row=2, column=4, pady=4)

        boost_btn_remv = Button(self, text="Remove", command=lambda: remove_from_list(boosted, self.boost_drop.get()))
        boost_btn_remv.grid(row=2, column=2)

        boost_btn_add = Button(self, text="Add", command=lambda: add_to_list(boosted, self.entry2.get(), self.entry2, defults["boost"]))
        boost_btn_add.grid(row=2, column=3)

        #########################################

        #degraded combo
        self.deg_drop = Combobox(self, postcommand=self.update_degraded)
        self.deg_drop['values'] = degraded
        self.deg_drop.current(0)
        self.deg_drop.grid(row=3, column=1, pady=1)
        self.entry3 = Entry(self)
        self.entry3.insert(0, "enter to lower priority")
        self.entry3.grid(row=3, column=4, pady=4)

        deg_btn_remv = Button(self, text="Remove", command=lambda: remove_from_list(degraded, self.deg_drop.get()))
        deg_btn_remv.grid(row=3, column=2)

        deg_btn_add = Button(self, text="Add", command=lambda: add_to_list(degraded, self.entry3.get(), self.entry3, defults["degrade"]))
        deg_btn_add.grid(row=3, column=3)

        ####
        #music combo

        self.music_drop = Combobox(self, postcommand=self.update_music)
        self.music_drop['values'] = music_list.keys()
        self.music_drop.current(0)
        self.music_drop.grid(row=4, column=1, pady=1)
        self.entry4 = Entry(self)
        self.entry4.insert(0, "enter url")
        self.entry4.grid(row=4, column=5)
        self.entry5 = Entry(self)
        self.entry5.insert(0, "enter song's name")
        self.entry5.grid(row=4, column=4)

        music_btn_remv = Button(self, text="Remove", command=lambda: remove_from_list(music_list, self.music_drop.get()))
        music_btn_remv.grid(row=4, column=2)

        music_btn_add = Button(self, text="Add", command=lambda: add_music(music_list, self.entry5.get(),self.entry4.get() ,self.entry5, defults["music"]))
        music_btn_add.grid(row=4, column=3)


        abtn = Button(self, text="Activate", command=scan_computer_programs)
        abtn.grid(row=1, column=5, sticky=E)

        sbtn = Button(self, text="Stop", command=lambda: stop_running(area, threads["procs"]))
        sbtn.grid(row=2, column=5, pady=6, sticky=E)

        cbtn = Button(self, text="Close", command=quit)
        cbtn.grid(row=3, column=5, pady=4, sticky=E)

        hbtn = Button(self, text="Save", command=save_lists)
        hbtn.grid(row=6, column=0, sticky=W)

        tsbtn = Button(self, text="TaskManager", command=lambda: os.system("TaskManager\pyProcMon.py"))
        tsbtn.grid(row=3, column=5, sticky=E)

        obtn = Button(self, text="start", command=lambda: call_running(area, threads["procs"], check_box))
        obtn.grid(row=6, column=5, sticky=E)


    def initUI_err(self):
        self.parent.title("Personal Helper")
        self.pack(fill=BOTH, expand=True)

    def update_boosted(self):
        self.boost_drop['values'] = boosted
        try:
            self.boost_drop.current(0)
        except:
            self.boost_drop.set("empty")


    def update_blocked(self):
        self.block_drop['values'] = working_bans
        try:
            self.block_drop.current(0)
        except:
            self.block_drop.set("empty")

    def update_degraded(self):
        self.deg_drop['values'] = degraded
        try:
            self.block_drop.current(0)
        except:
            self.block_drop.set("empty")


    def update_music(self):
        self.music_drop['values'] = music_list.keys()
        try:
            self.block_drop.current(0)
        except:
            self.block_drop.set("empty")





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
    root.geometry("700x300+200+200")
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


def call_running(area, thread1, check_val):
    if thread1 is not "empty":
        tkMessageBox.showinfo("Error", "already up")
    else:
        threads["procs"] = thread.start_new_thread(running_programs, (area, check_val))


#doing what task manager is doing' showing realtime processes
def running_programs(area, check_box):  # (add working):  #working is that the user doesnt want games and such to be reachable
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


            #proc_vals = str(line).split(" ")
            if proc_vals[0] not in process.keys():
                print proc_vals[0]
                process[proc_vals[0]] = proc_vals[1:]
            area.tag_configure('sys', background='light blue')





        #checking if working status is on and defusing processes if necessary
        if check_box["work"].get() == 1:
            for key in process.keys():
                #print 'Taskkill /IM ' + key + ' /F'
                if key in working_bans:
                    print "killing ", key
                    cmd = 'Taskkill /IM ' + key + ' /F'
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    process.pop(key)

        #Changing priority for processes the user chose

        if check_box["boost"].get() == 1:
            for proc in boosted:
                pids = get_pid(proc)
                set_priority(pids)
                print "wow!"
            for proc in degraded:
                pids = get_pid(proc)
                set_priority(pids, 0)



        print check_box["boost"].get()
        print check_box["work"].get()
        time.sleep(10)
        area.delete(*area.get_children())


def get_pid(name):
    pids = []
    for proc in psutil.process_iter():
        if proc.name() == name:
            pids.append(proc.pid)
    return pids

#in dev - must choose how to use
def set_priority(pids, priority=3):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    priority_classes = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]

    for pid in pids:
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, priority_classes[priority])


def play_music(url):
    webbrowser.open(url, 0, autoraise=False)
    time.sleep(0.1)
    pyautogui.keyDown("Alt")
    pyautogui.keyDown("Tab")
    pyautogui.keyUp("Alt")
    pyautogui.keyUp("Tab")

#will prevent cmd from popping up with ProcMon
def launch_Without_Console(command, args):
    """Launches 'command' windowless and waits until finished"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command]+args, startupinfo=startupinfo).wait()


def remove_from_list(list, item):
    if type(list) is ListType:
        if item in list:
            list.remove(item)
        else:
            tkMessageBox.showerror("error", "not in list "+item)
            print type(list)
    else:
        if item in list.keys():
            list.pop(item)
        else:
            tkMessageBox.showerror("error", "not in dict "+item)
            print type(list)


def add_to_list(list, item, entry, defult):
    if item not in list and item != "":
        list.append(item)
        print list
        entry.delete(0, END)
        entry.insert(0, defult)
    else:
        tkMessageBox.showerror("error", "already in the list "+item)
        print item

def add_music(dic, item_name, item_url,entery, defult):
    if item_name not in dic.keys():
        dic[item_name] = item_url
        entery.delete(0, END)
        entery.insert(0, defult)
    else:
        tkMessageBox.showerror("error", item_name+" is already in the list ")



def save_lists():
        block_file = open("Data/blocked.log", 'w')
        for line in working_bans:
            block_file.write(line+"\n")
        block_file.close()
        boosted_file = open("Data/boosted.log", 'w')
        for line in boosted:
            boosted_file.write(line+"\n")
        boosted_file.close()
        degraded_file = open("Data/degraded.log", 'w')
        for line in degraded:
            degraded_file.write(line+"\n")
        degraded_file.close()
        music_file =  open("Data/music_dic.log", 'w')
        for key in music_list :
            music_file.write(key+":"+music_list[key]+"\n")
        music_file.close()

        tkMessageBox.showinfo("Done", "saved all lists")


if __name__ == "__main__":
    root = Tk()
    main()
