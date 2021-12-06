# simulador de dados
import random

print("bienvenido al simulador de dados v0.1")
instrucciones = True

while True:
    if instrucciones:
        print("1. tirar un dado")
        print("2. tirar dos dados")
        print("3. repetir instrucciones")
        print("4. salir")
        instrucciones = False


    res = int(input())
    if res == 1:
        dado = random.randint(1, 6)
        print("El dado dio ",dado)

    elif res == 2:
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        print("El dado 1 dio ",dado1)
        print("El dado 2 dio ",dado2)
    
    elif res == 3:
        instrucciones = True
    
    elif res == 4:
        break