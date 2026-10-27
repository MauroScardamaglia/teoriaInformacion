import math

def imprimirMatriz(mat):
    for fila in mat: 
        for elemento in fila:
            print(f"{elemento:.2f}",end="\t\t")
        print()
    print()

def generarProbabilidadesPriori(entrada):
    alfabetoEnt = []
    for c in entrada:
        if c not in alfabetoEnt:
            alfabetoEnt += c

    probPriori = [0] * len(alfabetoEnt)

    for c in entrada:
        probPriori[alfabetoEnt.index(c)] += 1

    probPriori = [prob/sum(probPriori) for prob in probPriori]
    return probPriori

'''
2. Codificar una función en Python que reciba como parámetros dos cadenas de caracteres
que contengan secuencias de entrada y de salida de un canal y retorne la matriz que
representa dicho canal. '''

def generarMatrizProbabilidadesCondicionales(entrada,salida,mostrar=False): # recibe cadenas
    alfabetoEnt = []
    alfabetoSal = []
    for c in entrada:
        if c not in alfabetoEnt:
            alfabetoEnt += c


    for c in salida:
        if c not in alfabetoSal:
            alfabetoSal += c


    r = len(alfabetoEnt)
    s = len(alfabetoSal)
    matriz = [[0] * s for _ in range(r)]

    if (mostrar): imprimirMatriz(matriz)

    for a,b in zip(entrada,salida):
        i = alfabetoEnt.index(a)
        j = alfabetoSal.index(b)
        matriz[i][j] += 1

    if (mostrar): imprimirMatriz(matriz)

    for i in range(r):
        suma = sum(matriz[i])
        for j in range(s):
            matriz[i][j] /= suma

    if (mostrar): imprimirMatriz(matriz)
    return matriz

def ej3():
    entrada1 = "1101011001101010010101010100011111"
    salida1 = "1001111111100011101101010111110110"
    entrada2 = "110101100110101100110101100111110011"
    salida2 = "110021102110022010220121122100112011"

    probPriori1 = generarProbabilidadesPriori(entrada1)
    probPriori2 = generarProbabilidadesPriori(entrada2)

    mat1 = generarMatrizProbabilidadesCondicionales(entrada1,salida1)
    mat2 = generarMatrizProbabilidadesCondicionales(entrada2,salida2) 

    print("--- Ejercicio 3 ----\n")

    print("Entrada 1: ",entrada1)
    print("Salida 1: ",salida1)
    print("Probs priori1: ",probPriori1)
    print("Matriz de probabilidades condicionales 1")
    imprimirMatriz(mat1)
    

    print("\nEntrada 2: ",entrada2)
    print("Entrada 2: ",salida2)
    print("Probs priori2: ",probPriori2)
    print("Matriz de probabilidades condicionales 2")
    imprimirMatriz(mat2)

'''
    7. Realizar funciones en Python que reciban como parámetros: una lista con las
    probabilidades a priori y la matriz de probabilidades condicionales del canal, y devuelvan:
    a. Una lista con las probabilidades de los símbolos de salida
    b. Una matriz con las probabilidades a posteriori del canal
    c. Una matriz con las probabilidades de los eventos simultáneos '''

def generarListaProbabilidadesSalida(probabilidadesPriori,matriz): # P(Bj)
    print()

def generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matriz): # P(A/bj)
    print()

def generarMatrizProbabilidadesEventosSimultaneos(probabilidadesPriori,matriz): # ???
    print()


'''
    11. Desarrollar una función en Python que reciba como parámetros: una lista con las
    probabilidades a priori y la matriz de probabilidades condicionales del canal, y retorne una
    lista con las entropías a posteriori. '''

def entropiasPosteriori(probabilidadesPriori,matriz):
    print()

'''
    15. Implementar funciones en Python que reciban como parámetros: una lista con las
    probabilidades a priori y la matriz de probabilidades condicionales del canal, y calculen por
    definición (es decir, a partir de las probabilidades, no de sus relaciones):
    a. La equivocación o ruido
    b. La pérdida
    c. La entropía afín
    d. La información mutua '''


'''
    18. Realizar funciones booleanas en Python que reciban como parámetro la matriz de un canal
    y verifiquen si se trata de:
    a. Un canal sin ruido
    b. Un canal determinante '''


'''
    20. Implementar una función en Python que reciba como parámetros las matrices de dos
    canales y genere la matriz del canal compuesto por los canales en serie. '''



'''
    22. Desarrollar funciones en Python que reciban como parámetros: la matriz de un canal y los
    índices de dos columnas, y realicen lo siguiente:
    a. Verificar si las columnas se pueden combinar en una reducción suficiente
    b. Generar la matriz del canal determinante necesario para combinar las columnas '''

'''
    23. Codificar una función en Python que reciba como parámetro la matriz de un canal y,
    utilizando las funciones de los ejercicios 20 y 22, realice todas las reducciones suficientes
    posibles y devuelva la matriz del canal reducido '''


'''
    25. Implementar funciones en Python que reciban como parámetro la matriz de un canal y
    resuelvan lo siguiente:
    a. Verificar si se trata de un canal uniforme
    b. Calcular su capacidad en los siguientes casos:
    i. Canal determinante
    ii. Canal sin ruido
    iii. Canal uniforme '''

'''
    26. Realizar una función en Python que reciba como parámetros: la matriz de un canal binario
    y un valor de paso, y estime la capacidad del canal mediante el cálculo de la información
    mutua para un conjunto de probabilidades a priori distribuidas uniformemente según el
    paso especificado. La función debe retornar el valor de capacidad estimado, junto con su
    probabilidad asociada. '''


'''
    30. Desarrollar una función en Python que reciba como parámetros: una lista con
    probabilidades a priori y la matriz de un canal, y calcule la probabilidad de error utilizando
    la regla de decisión de máxima posibilidad. '''

def main():
    print("hallo, ich bin Mauro's Geist \n")
    ej3()

main()