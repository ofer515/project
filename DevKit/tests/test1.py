<<<<<<< HEAD
"""
import selenium.webdriver as webdriver

#FirefoxDriver driver = new FirefoxDriver();
#driver.manage().window().setPosition(new Point(-2000, 0));
browser = webdriver.PhantomJS()
#browser = webdriver.Firefox()

browser.get('https://www.youtube.com/watch?v=nJtiYPe9nv4')

"""




from selenium import webdriver


import pyautogui


# get initial window size
import time
import ctypes
user32 = ctypes.windll.user32
time.sleep(3)
top = user32.GetTopWindow(None)
print top

"""
driver = webdriver.Firefox()
driver.set_window_position(1000,1000)
#pyautogui.keyDown("Alt")
#pyautogui.keyDown("Tab")
#pyautogui.keyUp("Alt")
#pyautogui.keyUp("Tab")


driver.get("https://www.youtube.com")


#p.communicate(input=alt_tab)
driver.maximize_window()
#width = driver.get_window_size()["width"]
#height = driver.get_window_size()["height"]

#driver.set_window_position(width, height)
#driver.set_window_size(0, 0)




"""
"""
import webbrowser, time
import pyautogui


webbrowser.open("https://www.youtube.com/watch?v=iOxzG3jjFkY", 0, autoraise=False)

time.sleep(0.1)
pyautogui.keyDown("Alt")
pyautogui.keyDown("Tab")
pyautogui.keyUp("Alt")
pyautogui.keyUp("Tab")

"""

=======
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
>>>>>>> origin/master
