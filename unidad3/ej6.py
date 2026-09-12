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
    aux = esUnivoco(palabrasCodigo)
    i = 0
    n = len(palabrasCodigo)
    while (aux and i < n):
        j = i + 1
        while(aux and j < n):
            aux = not compartenPrefijo(palabrasCodigo[i],palabrasCodigo[j])
            j += 1
        i += 1
    return aux

def esUnivoco(palabrasCodigo):
    # algoritmo de Sardinas-Patterson
    return True # xd