import math
import random

#                           EJERCICIO 14   


# a) generar una lista que represente el vector estacionario de la fuente.
def imprimirMatriz(mat): # imprime visualmente comodo (??? qué decís chabón?)
    for fila in mat: 
        for elemento in fila:
            print(f"{elemento:.2f}",end="\t\t")
        print()
    print()

#acá estoy haciendo como sería la función 
def productoMatricial(matriz, vector):
    n = len(mat)
    vecAux = [0] * n
    for i in range(n):
        for j in range(n):
            vecAux[i] += mat[i][j] * vector[j]
    return vecAux

def cumpleTolerancia(vec1,vec2, tolerancia = 0.01):
    vec3 = [abs(x - y) for x,y in zip(vec1,vec2)]
    return max(vec3) < tolerancia

def vectorEstacionarioAprox(matriz, tolerancia = 0.01):
    n = len(matriz)
    vec = [1/n] * n
    cumpleTolerancia = False
    while(not cumpleTolerancia):
        vecAux = productoMatricial(matriz,vec)
        cumpleTolerancia = cumpleTolerancia(vec,vecAux,tolerancia)

def vectorEstacionario(matrizTransicion): 
    mat = [fila.copy() for fila in matrizTransicion]

    n = len(mat)
    for i in range(n):
        mat[i][i] -= 1
    for fila in mat:
        fila.append(0) # agrego un 1 en cada fila, representando el coeficiente de los vi
    print("Matriz  Ampliada (M-I) x V = 0")
    imprimirMatriz(mat)

    mat.pop() # saca la última fila -> equivale a del mat[-1] (último elemento) o del mat[n-1]
    # mat.insert(0,[1] * (n+1)) # agrego al sistema de ecuaciones la ecuacion v1 + v2 + .. + vn = 1
    mat.append([1] * (n+1))
    print("Sistema de ecuaciones (M-I) x V = 0, v1 + v2 + .. + vn = 1; descarto la última ecuación y la reemplazo por la de sumatoria = 1")
    imprimirMatriz(mat)


    #diagonalizar
    #en elementos debajo de la diagonal principal pongo 0's
    for j in range(0,n-1): # por cada columna
        for i in range(j+1,n):  # por cada fila en dicha columna pongo 0's
            aux = mat[i][j] / mat[j][j]
            mat[i] = [a - aux * b for a,b in zip(mat[i],mat[j])] # resto en la fila actual lo necesario para poner 0 en el elemento actual
    print("Matriz Diagonalizada")
    imprimirMatriz(mat)
    print()

    # generar Vector Estacionario
    V = [0] * n
    print(n)
    for i in range(n-1,-1,-1): # desde n-1 hasta 0 (inclusive)         
        for j in range(n-1,i,-1):
            mat[i][n] -= mat[i][j] * V[j]
        V[i] = mat[i][n] / mat[i][i]

    print("Vector estacionario: ",V, end="\n\n")
    return V

# b) calcular la entropía de la fuente
def entropiaMarkoviana(matrizTransicion, vectorEstacionario):
    suma = 0
    n = len(vectorEstacionario)
    for k in range(0,n):
        aux = 0
        for i in range(0,n):
            if (mat[i][k] != 0):
                aux += mat[i][k] * math.log2(1/mat[i][k])
        suma += vectorEstacionario[k] * aux
    return suma

#para inicializar la matriz en 0:
#mat = [[0] * n for _ in range(n)]

#                                       EJERCICIO 15

# a) Dada una cadena de caracteres que representa un mensaje emitido por una fuente,
# devolver una lista con su alfabeto y su matriz de transición.

def generarFuenteMarkoviana(cadena):
    alfabeto = []
    matriz = []
    # genero alfabeto
    for i in range(0,len(cadena)):
        if (cadena[i] not in alfabeto):
            alfabeto.append(cadena[i])
    n = len(alfabeto)
    matriz = [[0] * len(cadena) for _ in range[n]]

    # acumulo apariciones
    for i in range(1,len(cadena)):
        matriz[alfabeto.index(cadena[i-1])][alfabeto.index(cadena[i])] += 1

    # normalizo
    for k in range(0,n):
        suma = 0
        for i in range(0,n):
            suma += matriz[i][k]
        for i in range(0,n):
            matriz[i][k] /= suma

    return alfabeto, matriz

# b) Dados un número entero N, una lista que contenga el alfabeto de una fuente y su
# matriz de transición, simular la generación de una cadena de caracteres de longitud
# N emitida por esa fuente.

def devolverSimbolo(alfabeto, matriz,j):
    r = random.random()
    probAcumulada = 0.0
    for i in range(0,len(matriz)):
        if (r < probAcumulada + matriz[i][j]):
            return alfabeto[i]
        else:
            probAcumulada += matriz[i][j]

# el primer caracter lo genero equiprobablemente?
def generarCadena(n, alfabeto, matriz):
    cadena = ""
    r = random.random(0,len(matriz))
    cadena += alfabeto[math.floor(r)]
    for i in range(1,n):
        c = devolverSimbolo(alfabeto,matriz,alfabeto.index(cadena[i-1]))
        cadena += c

# c. Dada una matriz de transición y una tolerancia máxima, determinar si se trata de
# una fuente de memoria nula o una fuente con memoria.
def esNula(mat, tolerancia= 0.01): # es nula o no es nula, esa es la cuestión
    return cumpleTolerancia([max(fila) for fila in mat],[min(fila) for fila in mat],tolerancia)
        
        

mat = [
    [1/2, 1/3, 0],
    [1/2, 1/3, 1],
    [0, 1/3, 0]
]
print(mat,"\n") # imprime en una línea
imprimirMatriz(mat)

vectorEst = vectorEstacionario(mat)
entropia = entropiaMarkoviana(mat,vectorEst)
print(entropia)
print(esNula(mat),0.01)