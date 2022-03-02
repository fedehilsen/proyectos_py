from cgitb import text
import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
from turtle import resetscreen
import uuid
import pyperclip
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

backend = default_backend()
salt = b'2444'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt = salt,
    iterations = 100000,
    backend = backend
)

encryptionKey = 0

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(message: bytes, token: bytes) -> bytes:
    return Fernet(token).decrypt(message)



#codigo de base de datos
with sqlite3.connect("password_manager.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recoveryKey TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

#crear popup
def popUp(text):
    answer = simpledialog.askstring("input string", text)

    return answer



#Iniciar ventana
window = Tk()

window.title("Password Panager")


#agarrar la contraseña y hashearla
def hashpassword(input):
    hash = hashlib.sha256(input)
    hash = hash.hexdigest()

    #devolver la contraseña hasheada y legible
    return hash





#creacion de master password
def primera():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("250x180")

    lbl = Label(window, text="Create master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack(pady=5)
    txt.focus()

    lbl1 = Label(window, text="Repeat master password")
    lbl1.pack(pady=5)

    txt1 = Entry(window, width=20, show="*")
    txt1.pack(pady=5)

    lbl2 = Label(window)
    lbl2.pack(pady=5)


    #guardar la contraseña creada
    def savePassword():
        if txt.get() == txt1.get():

            sql = "DELETE FROM masterpassword WHERE id = 1"

            cursor.execute(sql)

            #mandar a hashear la contraseña
            hashedpassword = hashpassword(txt.get().encode('utf-8'))
            key = str(uuid.uuid4().hex)
            recoveryKey = hashpassword(key.encode('utf-8'))

            global encryptionKey
            encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))
            

            #indicar en donde va a ir la contraseña en la db
            insert_password = """INSERT INTO masterpassword(password, recoveryKey)
            VALUES(?, ?) """

            #mandar la contraseña a la db
            cursor.execute(insert_password, ((hashedpassword), (recoveryKey)))
            db.commit()


            recoveryScreen(key)


            #ir al manager
            #passwordvault()
        else:
            lbl2.config(text="Passwords dont match")



    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=5)

def recoveryScreen(key):
    for widget in window.winfo_children():
        widget.destroy()
        
    window.geometry("250x180")

    lbl = Label(window, text="Save this key to be able to recover account")
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window, text=key)
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=5)

    def copyKey():
        pyperclip.copy(lbl1.cget("text"))

    btn = Button(window, text="Copy Key", command=copyKey)
    btn.pack(pady=5)

    def done():
        passwordvault()

    btn = Button(window, text="Done", command=done)
    btn.pack(pady=5)

    
def resetScreen():
    for widget in window.winfo_children():
        widget.destroy()
        
    window.geometry("250x180")

    lbl = Label(window, text="Enter Recovery Key")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=5)

    def getRecoveryKey():
        recoveryKeyCheck = hashpassword(str(txt.get()).encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND recoverykey = ?", [(recoveryKeyCheck)])
        return cursor.fetchall()

    def checkRecoveryKey():
        checked = getRecoveryKey()
        if checked:
            primera()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Key")

    btn = Button(window, text="Check Key", command=checkRecoveryKey)
    btn.pack(pady=5)



#pantalla para poner la master password una vez que ya la hayas creado
def loginscreen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("250x140")

    lbl = Label(window, text="Enter master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack(pady=5)
    txt.focus()


    def getmasterpassword():

        #mandar a hashear la contraseña
        checkhashedpassword = hashpassword(txt.get().encode('utf-8'))

        global encryptionKey
        encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))


        #buscar en la db si existe el mismo hash
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkhashedpassword)])
        print(checkhashedpassword)
        return cursor.fetchall()

    #chequear si la contraseña coincide
    def checkPassword():
        match = getmasterpassword()

        print(match)

        if match:
            # ir al manager
            passwordvault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="wrong password")

    
    def resetPassword():
        resetScreen()

    btn = Button(window, text="Enter", command=checkPassword)
    btn.pack(pady=5)

    btn = Button(window, text="Reset password", command=resetPassword)
    btn.pack(pady=5)

    lbl1 = Label(window)
    lbl1.pack(pady=5)

#password manager
def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"

        website = encrypt(popUp(text1).encode(), encryptionKey)
        username = encrypt(popUp(text2).encode(), encryptionKey)
        password = encrypt(popUp(text3).encode(), encryptionKey)


        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordvault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordvault()

    window.geometry("700x350")


    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)

    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)



    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=80)

    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=80)

    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall != None):
        i=0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            if (len(array) == 0):
                break

            lbl1 = Label(window, text=(decrypt(array[i][1], encryptionKey)))
            lbl1.grid(column=0, row=i+3)

            lbl1 = Label(window, text=(decrypt(array[i][2], encryptionKey)))
            lbl1.grid(column=1, row=i+3)

            lbl1 = Label(window, text=(decrypt(array[i][3], encryptionKey)))
            lbl1.grid(column=2, row=i+3)

            btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i = i + 1

            cursor.execute("SELECT * FROM vault")
            if(len(cursor.fetchall()) <= i):
                break


#fijarte si existe una base de datos
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginscreen()
else:
    primera()
window.mainloop()