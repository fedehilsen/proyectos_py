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


#agarrar la contraseña y hashearla
def hashpassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    #devolver la contraseña hasheada y legible
    return hash





#creacion de master password
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


    #guardar la contraseña creada
    def savePassword():
        if txt.get() == txt1.get():

            #mandar a hashear la contraseña
            hashedpassword = hashpassword(txt.get().encode('utf-8'))
            

            #indicar en donde va a ir la contraseña en la db
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """

            #mandar la contraseña a la db
            cursor.execute(insert_password, [(hashedpassword)])
            db.commit()


            #ir al manager
            passwordvault()
        else:
            lbl2.config(text="Passwords dont match")



    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=5)



#pantalla para poner la master password una vez que ya la hayas creado
def loginscreen():
    window.geometry("250x120")

    lbl = Label(window, text="Enter master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack(pady=5)
    txt.focus()


    def getmasterpassword():

        #mandar a hashear la contraseña
        checkhashedpassword = hashpassword(txt.get().encode('utf-8'))

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

    btn = Button(window, text="Enter", command=checkPassword)
    btn.pack(pady=5)

    lbl1 = Label(window)
    lbl1.pack(pady=5)

#password manager
def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("700x350")

    lbl = Label(window, text="Password Vault")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=5)



#fiharte si existe una base de datos
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginscreen()
else:
    primera()
window.mainloop()