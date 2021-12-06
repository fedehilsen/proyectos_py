#juego random

import random

PrimerNumero = random.randint(1, 10)
print("Decidir si el siguiente numero va a ser menor o mayor del 1 al 10:")

while True:
    print(PrimerNumero)
    SegundoNumero = random.randint(1, 10)
    Res = int(input("Si es menor escribe 1 y si es mayor escribe 2: "))

    if Res == 1 and PrimerNumero > SegundoNumero:
        print("Bien")

    elif Res == 2 and PrimerNumero < SegundoNumero:
        print("Bien")

    elif PrimerNumero == SegundoNumero:
        print("Bien")

    else:
        print("perdiste el numero era ", SegundoNumero)
        break

    PrimerNumero = SegundoNumero