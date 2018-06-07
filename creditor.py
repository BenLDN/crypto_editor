#!/usr/bin/env python3

#my first GUI programme

from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def newf():
    global filen
    if filen!="" or box.get("1.0","end-1c")!="":
        answer=messagebox.askquestion("Save?","Save current file before?")
        if answer=='yes':
            savef()
    box.delete("1.0",END)
    filen=""
    status.config(text='New file created.')  

def openf():
    global filen, box, passw
    filen=filedialog.askopenfilename()
    file=open(filen,'r')
    boxText=decTxt(file.read(),passw)
    file.close()
    box.delete("1.0",END)
    box.insert(END,boxText)
    status.config(text='File opened.')    

def savef():
    global filen, box, passw
    if filen=="":
        filen=filedialog.asksaveasfilename()
    boxText=encTxt(box.get("1.0","end-1c"), passw)
    file=open(filen,'w')
    file.write(boxText)
    file.close()
    status.config(text='Saved.')

def saveasf():
    global filen, box, passw
    filen=filedialog.asksaveasfilename()
    boxText=encTxt(box.get("1.0","end-1c"), passw)
    file=open(filen,'w')
    file.write(boxText)
    file.close()
    status.config(text='Saved.')

def storePwnClose():
    global passw, e, coSub
    passw=e.get()
    coSub.destroy()
    status.config(text='Password changed')

def cryptoOptions():
    global enc, passw, e, coSub
    coSub=Tk()
    #coSub.iconbitmap(r'pandaicon.ico')
    coSub.title("Crypto Options")
    coSub.minsize(height=80, width=225)
    coText=Label(coSub, text="Enter the password to encrypt the file", anchor=W)
    coText.pack(side=TOP, fill=X)

    #encT=IntVar()
    #encT.set(1)
    
    #c1=Radiobutton(coSub, text="Yes", variable=encT, value=1)
    #c1.pack(anchor=W)
    #c2=Radiobutton(coSub, text="No", variable=encT, value=0)
    #c2.pack(anchor=W)

    e=Entry(coSub)
    e.insert(END, passw)
    e.pack()
    

    b=Button(coSub,text="OK", command=storePwnClose)
    b.pack()
    
    coSub.mainloop()

def main():

    global filen, enc, box, passw, status
    filen=''
    passw=''
    enc=True

    #main window
    root=Tk()
    #root.iconbitmap(r'pandaicon.ico')
    root.title("Crypto Editor")
    root.minsize(height=200, width=300)

    #status bar
    status=Label(root, text="Welcome to Red Crypto Editor", bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    #top menu
    topMenu=Menu(root)
    root.config(menu=topMenu)

    #file submenu
    subMenu=Menu(topMenu, tearoff=False)
    topMenu.add_cascade(label="File", menu=subMenu)
    subMenu.add_command(label="New", command=newf)
    subMenu.add_command(label="Open...", command=openf)
    subMenu.add_command(label="Save", command=savef)
    subMenu.add_command(label="Save As...", command=saveasf)
    subMenu.add_separator()
    subMenu.add_command(label="Exit", command=root.destroy)

    #crypto submenu
    cryptoMenu=Menu(topMenu, tearoff=False)
    topMenu.add_cascade(label="Crypto", menu=cryptoMenu)
    cryptoMenu.add_command(label="Options", command=cryptoOptions)

    #large text box with vertical scroll bar
    yscrollbar = Scrollbar(root)
    yscrollbar.pack(side=RIGHT, fill=Y)

    box=Text(root, yscrollcommand=yscrollbar.set)
    box.pack(side=TOP, expand=True, fill='both')

    root.mainloop()

def encTxt(text, pw):

    if pw=="":
        return text
    else:
        kdf=PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100000, backend=default_backend())
        key=base64.urlsafe_b64encode(kdf.derive(bytes(pw, 'utf-8')))

        f=Fernet(key)
        return str(f.encrypt(bytes(text,'utf-8')), 'utf-8')

def decTxt(text, pw):

    if pw=="":
        return text
    else:
        kdf=PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100000, backend=default_backend())
        key=base64.urlsafe_b64encode(kdf.derive(bytes(pw, 'utf-8')))

        f=Fernet(key)
        return str(f.decrypt(bytes(text,'utf-8')),'utf-8')


if __name__=="__main__":
    main()

