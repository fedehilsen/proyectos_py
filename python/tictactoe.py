# ta te ti con python

turno = 1.0
p1 = " "
p2 = " "
p3 = " "
p4 = " "
p5 = " "
p6 = " "
p7 = " "
p8 = " "
p9 = " "

while True:
    print("elegi una posicion (1-9)")

    print(p1,"|",p2,"|",p3)
    print("---------")
    print(p4,"|",p5,"|",p6)
    print("---------")
    print(p7,"|",p8,"|",p9)


    res = int(input(""))
    if turno.is_integer() == True:
        jugador = "x"
    else:
        jugador = "o"

    
    # poner en el numero que eligio

    if res == 1 and p1 == " ":
        p1 = jugador
        turno = turno + 0.5

    elif res == 2 and p2 == " ":
        p2 = jugador
        turno = turno + 0.5

    elif res == 3 and p3 == " ":
        p3 = jugador
        turno = turno + 0.5

    elif res == 4 and p4 == " ":
        p4 = jugador
        turno = turno + 0.5

    elif res == 5 and p5 == " ":
        p5 = jugador
        turno = turno + 0.5

    elif res == 6 and p6 == " ":
        p6 = jugador
        turno = turno + 0.5

    elif res == 7 and p7 == " ":
        p7 = jugador
        turno = turno + 0.5

    elif res == 8 and p8 == " ":
        p8 = jugador
        turno = turno + 0.5

    elif res == 9 and p9 == " ":
        p9 = jugador
        turno = turno + 0.5

    
    # resolucion

    # p1 | p2 | p3
    # ------------
    # p4 | p5 | p6
    # ------------
    # p7 | p8 | p9

    if p1 != " " and p1 == p2 and p1 == p3:
        print("el ganador es", p1)
        break

    elif p4 != " " and p4 == p5 and p4 == p6:
        print("el ganador es", p4)
        break

    elif p7 != " " and p7 == p8 and p7 == p9:
        print("el ganador es", p9)
        break

    elif p1 != " " and p1 == p4 and p1 == p7:
        print("el ganador es", p4)
        break

    elif p2 != " " and p2 == p5 and p2 == p8:
        print("el ganador es", p2)
        break
    
    elif p3 != " " and p3 == p6 and p3 == p9:
        print("el ganador es", p3)
        break

    elif p1 != " " and p1 == p5 and p1 == p9:
        print("el ganador es", p1)
        break

    elif p3 != " " and p3 == p5 and p3 == p7:
        print("el ganador es", p3)
        break