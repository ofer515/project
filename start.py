from Tkinter import *
import win32com.shell.shell as shell
import os


def main_window():
    window = Tk()
    window.geometry("500x500")
    window.iconbitmap(r"C:\Users\ofer\Desktop\github files\project\Alien_robot.ico")
    window.wm_title("Personal Helper!")
    l = Label(text="Personal helper!")
    b = Button(window, text="start scanning for programs", command=scan_computer_programs)
    l.pack()
    b.pack()
    window.mainloop()

def scan_computer_programs():
    privs = 'asadmin'
    filename = "programs_finder.py"
    if sys.argv[-1] != privs:
        script = os.path.dirname(filename) + os.path.basename(filename)
        print script
        params = ' '.join([script] + sys.argv[1:] + [privs])
        try:
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        except Exception as e:
            print e
            print "need admin"




if __name__ == "__main__":
    main_window()
