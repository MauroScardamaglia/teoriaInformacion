import math
import random

#                           EJERCICIO 14   


def imprimirMatriz(mat): # imprime visualmente comodo (??? qué decís chabón?)
    for fila in mat: 
        for elemento in fila:
            print(f"{elemento:.2f}",end="\t\t")
        print()
    print()


# esta funcion es un desastre, me costó un huevo hacerla, pero en principio funciona
# la tengo que mejorar/hacer más clara 
def vectorEstacionario(matrizTransicion): 
    # generar matriz que representa el sistema de ecuaciones
    mat = [fila.copy() for fila in matrizTransicion]

    n = len(mat)
    for i in range(n):
        mat[i][i] -= 1
    for fila in mat:
        fila.append(0) # agrego un 1 en cada fila, representando el coeficiente de los vi
    print("Matriz  Ampliada (M-I) x V = 0")
    imprimirMatriz(mat)

    mat.insert(0,[1] * (n+1)) # agrego al sistema de ecuaciones la ecuacion v1 + v2 + .. + vn = 1
    print("Sistema de ecuaciones (M-I) x V = 0, v1 + v2 + .. + vn = 1")
    imprimirMatriz(mat)
    
    print()

    # diagonalizar
    # en elementos debajo de la diagonal principal pongo 0's
    for j in range(0,n-1): # por cada columna
        for i in range(j+1,n):  # por cada fila en dicha columna pongo 0's
            aux = mat[i][j] / mat[j][j]
            mat[i] = [a - aux * b for a,b in zip(mat[i],mat[j])] # resto en la fila actual lo necesario para poner 0 en el elemento actual
    print("Matriz Diagonalizada")
    imprimirMatriz(mat)
    print()

    # generar Vector Estacionario
    
    #version anterior (sin considerar v1+..+vn = 1)
    '''    V = [0] * n
    for i in range(n-1,-1,-1): # desde n-1 hasta 0 (inclusive)         
        for j in range(n-1,i,-1):
            mat[i][n-1] -= mat[i][j] * V[j]
        V[i] = mat[i][n-1] / mat[i][i] '''

    #version actual (considerando v1+..+vn = 1)
    V = [0] * n
    print(n)
    for i in range(n-1,-1,-1): # desde n-1 hasta 0 (inclusive)         
        for j in range(n-1,i,-1):
            mat[i][n] -= mat[i][j] * V[j]
        V[i] = mat[i][n] / mat[i][i]

    print("Vector estacionario: ",V, end="\n\n")
    return V


#para inicializar la matriz en 0:
#mat = [[0] * n for _ in range(n)]


mat = [
    [1/2, 1/3, 0],
    [1/2, 1/3, 1],
    [0, 1/3, 0]
]


print(mat,"\n") # imprime en una línea
imprimirMatriz(mat)

vectorEstacionario(mat)
