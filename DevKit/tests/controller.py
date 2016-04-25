########################################################################
import psutil
import wx


import subprocess
from model import Process
from threading import Thread
#from wx.lib.pubsub import Publisher

# only in app's startup  module
from wx.lib.pubsub import setuparg1
# in all modules that use pubsub
from wx.lib.pubsub import pub as Publisher

########################################################################
sys_proc = ['System Idle Process','System']
            #'smss.exe','avgrsa.exe','avgcsrva.exe','csrss.exe','wininit.exe','winlogon.exe','services.exe','lsass.exe','lsm.exe']


class ProcThread(Thread):
    """
    Gets all the process information we need as psutil isn't very fast
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        Thread.__init__(self)
        self.start() 
        
    #----------------------------------------------------------------------
    def run(self):
        """"""
        pids = psutil.pids()
        print pids
        procs = []
        cpu_percent = 0
        mem_percent = 0
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() not in sys_proc:
                cpu = p.cpu_percent()
                mem = p.memory_percent()
                new_proc = Process(p.name,
                                   str(p.pid),
                                   "not implemented yet",
                                   "not yet",
                                   str(cpu),
                                   str(mem)
                                   )
                print new_proc
                procs.append(new_proc)
                cpu_percent += cpu
                mem_percent += mem


        # send pids to GUI
        wx.CallAfter(Publisher.sendMessage, "update", procs)

        number_of_procs = len(procs)
        wx.CallAfter(Publisher.sendMessage, "update_status",
                     (number_of_procs, cpu_percent, mem_percent))



    def run1(self):
        """"""
        cmd = 'WMIC PROCESS get Caption,Processid,Priority,workingsetsize'
        procsses = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cpu_percent = 0
        mem_percent = 0
        for proc in procsses:
            try:
                proc_vals = str(proc).split(" ")
                #cpu = p.get_cpu_percent()
                #mem = p.get_memory_percent()
                new_proc = Process(proc_vals[0],
                                   str(proc_vals[2]),
                                   #p.exe,
                                   "what?",
                                   "ofer",
                                   str(23),
                                   str(32)
                                   )
                print new_proc
                procs.append(new_proc)
                #cpu_percent += cpu
                #mem_percent += mem
            except Exception as e:
                print e

        print procs
        # send pids to GUI
        wx.CallAfter(Publisher.sendMessage, "update", procs)

        number_of_procs = len(procs)
        wx.CallAfter(Publisher.sendMessage, "update_status",
                     (number_of_procs, cpu_percent, mem_percent))


if __name__ == "__main__":
    run()