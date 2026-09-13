'''
6. Desarrollar funciones booleaneas en Python que reciban como parámetro una lista con
palabras código y verifiquen si el código es:
a. no singular
b. instantáneo
c. unívocamente decodificable
'''

def esNoSingular(palabrasCodigo):
    aux = True
    i = 0
    n = len(palabrasCodigo)
    while (aux and i < n):
        j = i + 1
        while(aux and j < n):
            aux = (palabrasCodigo[i] != palabrasCodigo[j])
            j += 1
        i += 1
    return aux

def compartenPrefijo(cad1,cad2):
    if (len(cad1) < len(cad2)): #(el código posterior asume que cad1 >= cad2)
        cadAux = cad1
        cad1 = cad2
        cad2 = cadAux
    return cad2 == cad1[0:len(cad2)]


def esInstantaneo(palabrasCodigo):
    aux = esUnivoco(palabrasCodigo) # si el alfabeto código no es univoco entonces no es instantáneo
    i = 0
    n = len(palabrasCodigo)
    while (aux and i < n):
        j = i + 1
        while(aux and j < n):
            aux = not compartenPrefijo(palabrasCodigo[i],palabrasCodigo[j])
            j += 1
        i += 1
    return aux

def sufijo(cad1,cad2): # devuelve el sufijo, en caso de no compartir prefijo devuelve "" (cadena vacía)
    suf = ""
    if (compartenPrefijo(cad1,cad2)):
        if (len(cad1) < len(cad2)): #(el código posterior asume que cad1 >= cad2)
            cadAux = cad1
            cad1 = cad2
            cad2 = cadAux
        suf += cad1[len(cad2):] # asigna el sufijo de cad1
    return suf

def esUnivoco(palabrasCodigo):
    if (not esNoSingular(palabrasCodigo)):
        return False
    # algoritmo de Sardinas-Patterson
    conjSuf = [] # lista de conjuntos/sets S=[S1, S2, .., Sn] siendo Si={el1,el2,..,eln}
    conjSuf.append(set(palabrasCodigo))
    k = 0
    auxBool = True # booleano condición de corte
    while(auxBool): # acá podría haber un while(True) y no haría diferencia
        l1 = list(conjSuf[0])
        l2 = list(conjSuf[k])
        conjSuf.append(set())
        for x in l1:
            for y in l2:
                suf = sufijo(x,y)
                if (suf!=""):
                    conjSuf[k+1].add(suf)
        k += 1
        # 2 posibles condiciones de corte
        # a -> Sk == Sj para algun j pert[0-k] -> Univoco -> auxBool = False (cortá)
        # b -> z pert S0, para algún z pert a Sk -> noUnivoco -> auxBool = False (cortá)

        # b
        l3 = list(conjSuf[k])
        z = 0
        while(auxBool and z < len(l3)):
            auxBool = l3[z] not in conjSuf[0]
            z += 1
        if (not auxBool):
            return False

        # a
        j = 1
        while(auxBool and j < len(conjSuf) - 1): # interesa analizar desde j = 1 hasta j = k-1
            auxBool = not(conjSuf[j] == conjSuf[k])
            j += 1
        if(not auxBool):
            return True

def ej7():
    print()
    cadenas = [
        ["011","000","010","101","001","100"],
        ["110","100","101","001","110","010"],
        ["10","1100","0101","1011","0","110"],
        ["1101","10","1111","1100","1110","0"],
        ["011","0111","01","0","011111","01111"],
        ["1110","0","110","1101","1011","10"]
    ]
    
    print("----------------- Ejercicio 7 -----------------")
    for i,x in zip(range(len(cadenas)),cadenas):
        print(f"Código {i}: {x}")
        if (esInstantaneo(x)):
            print("Instantáneo")
        elif (esUnivoco(x)):
            print("Unívoco/Unívocamente Decodificable")
        elif(esNoSingular(x)):
            print("No Singular")
        else:
            print("Código Bloque")
        print()
    print()

def ej8():
    cadenas = [
        ["==","<","<=",">",">=","<>"],
        [")","[]","]]","([","[()]", "([)]"],
        ["/","*","-","*","++","+-"],
        [".;",";",",,",":","...",",:;"]
    ]
    
    print("----------------- Ejercicio 8 -----------------")
    for i,x in zip(range(len(cadenas)),cadenas):
        print(f"Código {i}: {x}")
        if (esInstantaneo(x)):
            print("Instantáneo")
        elif (esUnivoco(x)):
            print("Unívoco/Unívocamente Decodificable")
        elif(esNoSingular(x)):
            print("No Singular")
        else:
            print("Código Bloque")
        print()
    print()

ej7()
ej8()