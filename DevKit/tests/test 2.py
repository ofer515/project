__author__ = 'ofer'


import Tkinter as tkinter
root = tkinter.Tk()
comb = tkinter.
lst1 = ['Option1','Option2','Option3']
var1 = tkinter.StringVar()
drop = tkinter.OptionMenu(root,var1,*lst1)
drop.
drop.pack()
tkinter.mainloop()