from tkinter import *

root = Tk()
root.title("calculadora")

def calcular():
    print("hola")


b1 = Button(root, text="1", padx=40, pady=20, command=calcular)
b2 = Button(root, text="2", padx=40, pady=20, command=calcular)
b3 = Button(root, text="3", padx=40, pady=20, command=calcular)
b4 = Button(root, text="4", padx=40, pady=20, command=calcular)
b5 = Button(root, text="5", padx=40, pady=20, command=calcular)
b6 = Button(root, text="6", padx=40, pady=20, command=calcular)
b7 = Button(root, text="7", padx=40, pady=20, command=calcular)
b8 = Button(root, text="8", padx=40, pady=20, command=calcular)
b9 = Button(root, text="9", padx=40, pady=20, command=calcular)
b0 = Button(root, text="0", padx=91, pady=20, command=calcular)
bmas = Button(root, text="+", padx=38.4, pady=20, command=calcular)
bigual = Button(root, text="=", padx=91, pady=20, command=calcular)
bborrar = Button(root, text="del", padx=32, pady=20, command=calcular)

b1.grid(row=3, column=0)
b2.grid(row=3, column=1)
b3.grid(row=3, column=2)

b4.grid(row=2, column=0)
b5.grid(row=2, column=1)
b6.grid(row=2, column=2)

b7.grid(row=1, column=0)
b8.grid(row=1, column=1)
b9.grid(row=1, column=2)

b0.grid(row=4, column=1, columnspan=2)
bmas.grid(row=4, column=0)

bborrar.grid(row=5, column=0)
bigual.grid(row=5, column=1, columnspan=2)

escribir = Entry(root, width=35, borderwidth=5)
escribir.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


root.mainloop()