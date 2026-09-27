from ej6 import *
import math
import random

'''
9. Dada una lista que contiene las palabras código de una codificación, implementar
funciones en Python que resuelvan lo siguiente:
a. obtener una cadena de caracteres con el alfabeto código.
b. generar otra lista con las longitudes de las palabras (utilizar comprensión de listas).
c. calcular la sumatoria de la inecuación de Kraft (utilizar las funciones anteriores).
'''
# 
# a.
def obtenerAlfabetoCodigo(palabrasCodigo):
    alfabetoCodigo = []
    for palabra in palabrasCodigo:
        for caracter in palabra:
            if caracter not in alfabetoCodigo:
                alfabetoCodigo.append(caracter)
    return alfabetoCodigo

# b.
def obtenerLongitudes(palabrasCodigo):
    return [len(palabra) for palabra in palabrasCodigo]

# c.
def sumatoriaKraft(palabrasCodigo):
    alfabetoCodigo = obtenerAlfabetoCodigo(palabrasCodigo)
    longitudes = obtenerLongitudes(palabrasCodigo)
    suma = 0
    r = len(alfabetoCodigo)
    for long in longitudes:
        suma += r ** -long
    return suma

# 10. Calcular las sumatorias de la inecuación de Kraft de los
# códigos de los ejercicios 7 y 8
# Analizar los resultados obtenidos en función de su clasificación.
def ej10():
    cadenasEj7 = [
            ["011","000","010","101","001","100"],
            ["110","100","101","001","110","010"],
            ["10","1100","0101","1011","0","110"],
            ["1101","10","1111","1100","1110","0"],
            ["011","0111","01","0","011111","01111"],
            ["1110","0","110","1101","1011","10"]
        ]

    cadenasEj8 = [
            ["==","<","<=",">",">=","<>"],
            [")","[]","]]","([","[()]", "([)]"],
            ["/","*","-","*","++","+-"],
            [".;",";",",,",":","...",",:;"]
        ]
    print("------------- EJERCICIO 10 -------------\n")
    print("------------- Cadenas del ej7 -------------\n")
    for i,cad in zip(range(len(cadenasEj7)),cadenasEj7):
        print(f"Palabras Código[{i}] = {cad}")
        kraft = sumatoriaKraft(cad)
        print(f"Sumatoria de Kraft: {kraft:.2f}")
        if (kraft > 1):
            print("Unívocamente Imposible")
        else:
            print("Existe al menos un código instantáneo con dichas longitudes")
        print()
    print("\n\n")

    print("------------- Cadenas del ej8 -------------\n")
    for i,cad in zip(range(len(cadenasEj8)),cadenasEj8):
        print(f"Palabras Código[{i}] = {cad}")
        kraft = sumatoriaKraft(cad)
        print(f"Sumatoria de Kraft: {kraft:.2f}")
        if (kraft > 1):
            print("Unívocamente Imposible")
        else:
            print("Existe al menos un código instantáneo con dichas longitudes")
        print()
    print("\n\n")


#11. Dadas dos listas paralelas que contengan las palabras código de una codificación y sus
#respectivas probabilidades, codificar funciones en Python que calculen:
#a. la entropía de la fuente
#b. la longitud media del código

# a
def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

def obtenerEntropia(palabrasCodigo,probabilidades):
    suma = 0
    alfabetoCodigo = obtenerAlfabetoCodigo(palabrasCodigo)
    r = len(alfabetoCodigo)
    infs = generarListaInformacion(probabilidades,r)
    for x, y in zip(probabilidades, infs):
        suma += x*y
    return suma

#b 
def longMedia(palabrasCodigo, probabilidades):
    return sum([prob * len(palabra) for palabra,prob in zip(palabrasCodigo, probabilidades)])

#12. Calcular la entropía de la fuente y la longitud media de cada código del ejercicio 8. Analizar
#los resultados obtenidos en función de su clasificación.
def ej12():
    cadenasEj8 = [
            ["==","<","<=",">",">=","<>"],
            [")","[]","]]","([","[()]", "([)]"],
            ["/","*","-","*","++","+-"],
            [".;",";",",,",":","...",",:;"]
        ]
    probabilidades = [0.1,0.5,0.1,0.2,0.05,0.05]
    print("------------- EJERCICIO 12 -------------\n")
    print("------------- Cadenas del ej8 -------------\n")
    for i,cad in zip(range(len(cadenasEj8)),cadenasEj8):
        print(f"Palabras Código[{i}] = {cad}")
        r = len(obtenerAlfabetoCodigo(cad))
        entropia = obtenerEntropia(cad,probabilidades)
        print(f"Entropia base {r}: {entropia:.2f}")
        longitudMedia = longMedia(cad, probabilidades)
        print(f"Longitud Media (L) = {longitudMedia:.2f}")
        # no sé como analizar estos resultados..
#        if (longitudMedia == entropia):
#            print("Código ")
#        else:
#            print("Existe al menos un código instantáneo con dichas longitudes")
        print()
    print("\n\n")



def ej13():
    simbolos1 = ["A","B","C","D"]
    simbolos2 = ["1","2","3","4"]

    probs1 = [0.5,0.25,0.125,0.125]
    probs2 = [0.333,0.333,0.167,0.167]

    codigo1a = ["0","10","110","111"]
    codigo2a = ["00","01","10","11"]
    codigo1b = ["1","2","30","31"]
    codigo2b = ["1","2","30","31"]

    codigos = [codigo1a,codigo2a,codigo1b,codigo2b] 
    probs = [probs1,probs2,probs1,probs2]
    simbolos = [simbolos1,simbolos2,simbolos1,simbolos2]

    print("\n\n ------- EJERCICIO 13 (comprobación de ser Compacto) ---------\n")
    for x,y,z in zip(codigos,probs,simbolos):
        print(f"Símbolos: {z}")
        print(f"Probabilidades: {y}")
        print(f"Código: {x}")
        if (esCompacto(x,y)):
            print("Es compacto\n")
        else:
            print("No es compacto \n")


#14. Realizar una función booleana en Python que reciba como parámetros dos listas paralelas
#que contengan las palabras código de una codificación y sus respectivas probabilidades, y
#determine si se trata de un código compacto.

def esCompacto(palabrasCodigo, probabilidades):
    aux = esUnivoco(palabrasCodigo)
    r = len(obtenerAlfabetoCodigo(palabrasCodigo))
    longs = obtenerLongitudes(palabrasCodigo)
    infs = generarListaInformacion(probabilidades,r)
    i = 0
    while (aux and i < len(palabrasCodigo)):
        aux = longs[i] <= math.ceil(infs[i])
        i += 1
    return aux


def ej15():
    cadenasEj8 = [
            ["==","<","<=",">",">=","<>"],
            [")","[]","]]","([","[()]", "([)]"],
            ["/","*","-","*","++","+-"],
            [".;",";",",,",":","...",",:;"]
        ]
    probabilidades = [0.1,0.5,0.1,0.2,0.05,0.05]
    print("\n\n\n------------- EJERCICIO 15 -------------\n")
    print("------------- Cadenas del ej8 -------------\n")
    for i,x in zip(range(len(cadenasEj8)),cadenasEj8):
        print(f"Código [{i+1}]: {x}")
        
        if (esCompacto(x,probabilidades)):
            print("Es compacto")
        else:
            print("No es compacto",end="")
            if (esUnivoco(x)):
                print()
            else:
                print(", porque no es unívoco")
        print()
    print()



#16. Implementar una función en Python que reciba como parámetros: un número entero N y
#    dos listas paralelas que contengan las palabras código de una codificación y sus
#    respectivas probabilidades, y genere aleatoriamente un posible mensaje de N símbolos
#    codificados emitido por dicha fuente.

def devolverPalabra(palabrasCodigo,probabilidades):
    r = random.random()
    probAcumulada = 0.0
    i = 0
    while (r >= probAcumulada + probabilidades[i]):
        probAcumulada += probabilidades[i]
        i += 1
    return palabrasCodigo[i]


def generarMensaje(n,palabrasCodigo,probabilidades):
    cad = ""
    for i in range(n):
        cad += devolverPalabra(palabrasCodigo,probabilidades)
        cad += " "
    return cad

def main():
    ej10()
    ej12()
    ej13()
    ej15()
    print(generarMensaje(4,["pelotuda","titanio","huerta","frenesí"],[0.125,0.5,0.25,0.125]))
    print(generarMensaje(8,["0","10","110","111"],[0.5,0.25,0.125,0.125]))

main()