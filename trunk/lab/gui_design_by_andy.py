from Tkinter import *
import string
from time import sleep

class DeviceList(Frame):
    def __init__(cls, items, method, parent=None):
        Frame.__init__(cls, parent)
        cls.pack(expand=YES, fill=BOTH, padx=5, pady=5)
        cls.makeWidgets(items)
        cls.__method=method
    def handleList(cls, event):
        index=cls.__listbox.curselection()
        index=cls.__listbox.curselection()
        path=cls.__listbox.get(index)
        cls.__method(path)
    def makeWidgets(cls, options):
        sbar=Scrollbar(cls)
        list=Listbox(cls, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        for label in options:
            list.insert(END, label)
        list.select_set(0)
        list.config(selectmode=SINGLE, setgrid=1)
        list.bind('<Button-1>', cls.handleList)
        cls.__listbox=list

class DeviceDetail(Frame):
    def __init__(cls, items, parent=None):
        Frame.__init__(cls, parent)
        cls.pack(expand=YES, fill=BOTH, padx=5, pady=5)
        cls.__list=[]
        cls.update(items)
    def update(cls, items):
        cls.clear()
        for (key, value) in items.items():
            f=Frame(cls)
            k=Label(f, text=key, bg='white', fg='black', relief=SUNKEN, width=15)
            k.pack(side=LEFT, expand=YES, fill=X, padx=5)
            v=Label(f, text=value, bg='white', fg='black', relief=SUNKEN, width=40)
            v.pack(side=LEFT, expand=YES, fill=X, padx=5)
            f.pack(side=TOP, expand=YES, fill=X, pady=2)
            cls.__list.append(f)
    def clear(cls):
        if cls.__list!=[]:
            for i in cls.__list:
                i.pack_forget()

if __name__=='__main__':
    def handle(d):
        for i in list:
            dict[a[i]]+=100
        d.update(dict)
    dict={}
    a='abcdefghijklmn'
    list=range(10)
    for i in list:
        dict[a[i]]=i
    root=Tk()
    d=DeviceDetail(dict, root)
    d.pack(side=TOP)
    Button(root, text='update', command=(lambda d=d:handle(d))).pack(side=TOP)
    root.mainloop()
    
