
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get('http://www.yahoo.com')
assert 'Yahoo' in browser.title

elem = browser.find_element_by_name('p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()
"""
import webbrowser
import tkMessageBox
try:
    new = 2
    url = "https://www.youtube.com/watch?v=ZcoqR9Bwx1Y"
    webbrowser.open(url,new=new, autoraise=False)
except Exception as e:
    tkMessageBox.showinfo('hi', e)
    """