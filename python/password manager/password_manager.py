import sqlite3, hashlib
from tkinter import *

#codigo de base de datos
with sqlite3.connect("password_manager.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")



#Iniciar ventana
window = Tk()

window.title("Password Panager")

def hashpassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

def primera():
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

    def savePassword():
        if txt.get() == txt1.get():
            hashedpassword = hashpassword(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedpassword)])
            db.commit()

            passwordvault()
        else:
            lbl2.config(text="Passwords dont match")



    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=5)




def loginscreen():
    window.geometry("250x120")

    lbl = Label(window, text="Enter master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack(pady=5)
    txt.focus()

    def getmasterpassword():
        checkhashedpassword = hashpassword(txt.get().encode('utf-8'))

        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkhashedpassword)])
        print(checkhashedpassword)
        return cursor.fetchall()

    def checkPassword():
        match = getmasterpassword()

        print(match)

        if match:
            passwordvault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="wrong password")

    btn = Button(window, text="Enter", command=checkPassword)
    btn.pack(pady=5)

    lbl1 = Label(window)
    lbl1.pack(pady=5)


def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("700x350")

    lbl = Label(window, text="Password Vault")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=5)




cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginscreen()
else:
    primera()
window.mainloop()