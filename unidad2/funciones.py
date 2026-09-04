''' 1. Dada una lista que representa una distribución de probabilidades de una fuente de
memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:

a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
comprensión de listas).

b. obtener la entropía de la fuente (utilizar la función anterior).


2. Implementar funciones en Python que resuelvan lo siguiente:

a. Dada una cadena de caracteres que representa un mensaje emitido por una fuente
de memoria nula, devolver dos listas paralelas que contengan: el alfabeto de la
fuente y las probabilidades de cada símbolo.

b. Dados un número entero N, una lista que contenga el alfabeto de una fuente y otra
con las probabilidades de cada símbolo, simular la generación de una cadena de
caracteres de longitud N emitida por esa fuente
'''

'''
lista = ['a','b','c']
tupla = ('a','b','c')
'''

import math
import random

#                                                       EJERCICIO 1

# ya con este primer ejercicio me recomendaron que harcodeé los datos de una y ni me preocupe por las "malas prácticas",
# mientras el código funcione y yo lo entienda y pueda cambiar rapidamente

def generarProbabilidades():
    print("Ingrese cantidad de símbolos")
    n = input()
    total = 0

    for i in range(0,n):
        print("Ingrese probabilidad/cantidad de apariciones del símbolo " + i)
        Probabilidades[i] = input()
        total += Probabilidades[i] 

    if (total > 1):
        Probabilidades = [i / total for i in probabilidades]

    return Probabilidades

# a)
def generarListaInformacion(probabilidades):
    return [math.log2(1/prob) if prob > 0 else 0 for prob in probabilidades]

#b)
def entropia(probabilidades, informaciones):
    suma = 0
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

# b) este no funca, no sé porqué
#def entropia(probabilidades, informaciones):
#    sum([x * y for x, y in zip(probabilidades, informaciones)])

#main trucho
print("             EJERCICIO 1 \n")
probabilidades = [0.25, 0.125, 0.5, 0.125]   

print(probabilidades)

''' 
esto es una tupla, no se puede ni agregar/quitar elementos, ni cambiar sus valores (lista de constantes)
probabilidades = (0.25, 0.125, 0.5, 0.125)
probabilidades[2] = 1
probabilidades.append(2)
'''

print("P = ", probabilidades)
informaciones = generarListaInformacion(probabilidades)

print("I = ", informaciones)
print("Entropía: \n\n", entropia(probabilidades, informaciones))






#                                                      EJERCICIO 2

# a)
def generarFuente(cadena):
    total = 0
    alfabeto = []
    probabilidades = []
    for i in cadena:
        if (i not in alfabeto):
            alfabeto.append(i)
            probabilidades.append(0)
        probabilidades[alfabeto.index(i)] += 1
        total += 1
    probabilidades = [prob / total for prob in probabilidades]

    return alfabeto, probabilidades

# podría hacer una lista de probabilidades acumuladas, sirve para debuggear también
def devolverSimbolo(alfabeto, probabilidades):
    r = random.random()
    probAcumulada = 0.0
    for x, y in zip(alfabeto, probabilidades):
        if (r < probAcumulada + y):
            return x
        else:
            probAcumulada += y

def generarCadena(alfabeto, probabilidades, n):
    cadena = ""
    for i in range(0,n):
        c = devolverSimbolo(alfabeto, probabilidades)
        cadena += c
    return cadena    


print("             EJERCICIO 2 \n")

#cadena = "abaacddecdcabcbaa"
cadena = input("Ingrese cadena que sea la muestra para generar la fuente\n")
print("Cadena original: ",cadena)
print("Largo de la cadena: ",len(cadena),"\n")

alfabeto, probabilidades = generarFuente(cadena)
print("Alfabeto = ", alfabeto)
print("Probabilidades = ", probabilidades,"\n")

informaciones = generarListaInformacion(probabilidades)
print("I = ", informaciones)
print("Entropía: \n\n", entropia(probabilidades, informaciones))

print("Ingrese largo de la cadena aleatoria a generar")
n = int(input())
print(f"Cadena aleatoria: \"", generarCadena(alfabeto, probabilidades, n),"\"", sep="")

print("ej3b")
probabilidades = [1/9, 1/6, 1/9, 1/9, 1/6, 1/3]
informaciones = generarListaInformacion(probabilidades)
entr = entropia(probabilidades, informaciones)

print("Probabilidades: ", probabilidades)
print("Informaciones: ", informaciones)
print("Entropía", entr)


#                                                      EJERCICIO 8

def entropiaBinaria(w): # en realidad es omega, no w, pero bueno
    probs = [w,1-w]
    infs = generarListaInformacion(probs)
    print("\nProbs =",probs,"\nInfs= ",infs)
    return entropia(probs, infs) # tmb se podia hacer return w*math.log2(1/w) + (1-w)*math.log2(1/(1-w))

print("\n\n\n\nIngrese probabilidad w")
w = input()
w = float(w)
print("Entropia: ",entropiaBinaria(w),"\n\n")