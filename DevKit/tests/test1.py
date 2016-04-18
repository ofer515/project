import psutil

def process():
    s =psutil.Process(0)

    print s.name
    raw_input()
    plist = list(psutil.process_iter())
    plist = sorted(plist, key=lambda i: i.name)
    for i in plist:
        try:
            #psutil.Process.cpu
            print i.exe ,"  23"
            print i.cpu_percent(interval = 0.1) ,"  2"
            print i.memory_percent() ,"  1"
        except Exception as e:
            print e ,"asdasdsad"
            #print "'%s' Process is not allowing us to view the CPU Usage!" % i.name


def main():
    process()

main()