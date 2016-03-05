
import subprocess
cmd = 'WMIC PROCESS get Caption,Processid,Priority,workingsetsize'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
print proc
for line in proc.stdout:
        print line
