import math

def imprimirLista(lista,cantDecimales=4):
    n = len(lista)
    print("[",end="")
    for i in range(n-1):
        print(f"{lista[i]:.{cantDecimales}f},\t",end="")
    print(f"{lista[n-1]:.{cantDecimales}f}]")

def imprimirMatriz(mat,cantDecimales=4,alfabetoEnt=[],alfabetoSal=[],mostrar=False): #el código queda medio asquete, pero queda pipí cucú la matriz por consola
    m = len(mat[0])
 
    if (mostrar):
        print("\t",end="")
        for j in range(m):
            print("  ",end="")
            print(alfabetoSal[j],"\t\t\t",end="")
        print("\n\t",end="")

    for j in range(m):
        print("------------------------",end="")
    print()
    
    for i,fila in zip(range(len(mat)),mat): 
        if (mostrar):
            print(alfabetoEnt[i],end="\t")
            
        print("|",end="")
        for elemento in fila:
            print(f" {elemento:.{cantDecimales}f}",end="")
            if (cantDecimales<4):
                print(end="\t\t\t|")            
            else:
                print(end="\t\t|")

        print()
        if (mostrar):
            print("\t",end="")
        for j in range(m):
            print("------------------------",end="")
        print()
            
    print()
    

# me las traje del tp4
def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

def obtenerEntropia(probabilidades, r):
    suma = 0
    informaciones = generarListaInformacion(probabilidades,r)
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma
    

def generarProbabilidades(cadena):
    alfabeto = []
    for c in cadena:
        if c not in alfabeto:
            alfabeto += c

    probs = [0] * len(alfabeto)

    for c in cadena:
        probs[alfabeto.index(c)] += 1

    probs = [prob/sum(probs) for prob in probs]
    return probs

def obtenerAlfabetos(entrada,salida):
    alfabetoEnt = []
    alfabetoSal = []
    for c in entrada:
        if c not in alfabetoEnt:
            alfabetoEnt += c


    for c in salida:
        if c not in alfabetoSal:
            alfabetoSal += c
    
    return alfabetoEnt,alfabetoSal

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
    # si hago [[0] * s] * r -> quedan r referencias a la misma lista

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

    probPriori1 = generarProbabilidades(entrada1)
    probPriori2 = generarProbabilidades(entrada2)

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

def generarProbabilidadesSalida(probabilidadesPriori,matrizCanal): # P(B)
    probSalida = []
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    for j in range(s):
        probSalida.append(0)
        for i in range(r):
            probSalida[j] += probabilidadesPriori[i] * matrizCanal[i][j]
            
    return probSalida



def generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matrizCanal): # P(ai/bj)
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    matrizPosteriori = [[0] * s for _ in range(r)]
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    
    for i in range(r):
        for j in range(s):
            matrizPosteriori[i][j] = (matrizCanal[i][j] * probabilidadesPriori[i]) / probsSalida[j]
            
    return matrizPosteriori

def generarMatrizProbabilidadesEventosSimultaneos(probabilidadesPriori,matrizCanal): # P(ai,bj)
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    matrizEventosSimultaneos = [[0] * s for _ in range(r)]
    
    for i in range(r):
        for j in range(s):
            matrizEventosSimultaneos[i][j] = matrizCanal[i][j] * probabilidadesPriori[i]
            
    return matrizEventosSimultaneos

def auxMostrarProbsSalida(entrada,salida):
    print("Entrada: ",entrada)
    print("Salida: ",salida)
    probsPriori = generarProbabilidades(entrada)
    matrizCanal = generarMatrizProbabilidadesCondicionales(entrada,salida)
    print("Probs Priori: ",probsPriori)
    print("Matriz del Canal ")
    imprimirMatriz(matrizCanal)
    print()
    print("Probs de Salida (a partir de secuencia de salida): ",generarProbabilidades(salida))
    probsSalida = generarProbabilidadesSalida(probsPriori,matrizCanal)
    print("Probs de Salida (a partir de probs de salida y matriz del canal): ",probsSalida)
    
def auxMostrarProbsPosteriori(entrada,salida):
    probsPriori = generarProbabilidades(entrada)
    matrizCanal = generarMatrizProbabilidadesCondicionales(entrada,salida)
    matrizProbsPosteriori = generarMatrizProbabilidadesPosteriori(probsPriori,matrizCanal)
    print("-- Matriz Probabilidades a Posteriori P(ai/bj) --")
    alfabetoEnt,alfabetoSal= obtenerAlfabetos(entrada,salida)
    imprimirMatriz(mat=matrizProbsPosteriori,cantDecimales=4,alfabetoEnt=alfabetoEnt,alfabetoSal=alfabetoSal,mostrar=True)
    print("\n\n")

def auxMostrarProbsSimultaneas(entrada,salida):
    probsPriori = generarProbabilidades(entrada)
    matrizCanal = generarMatrizProbabilidadesCondicionales(entrada,salida)
    matrizProbsSimultaneas = generarMatrizProbabilidadesEventosSimultaneos(probsPriori,matrizCanal)
    print("-- Matriz Probabilidades de Eventos Simultáneos P(ai,bj) --")
    alfabetoEnt,alfabetoSal= obtenerAlfabetos(entrada,salida)
    imprimirMatriz(mat=matrizProbsSimultaneas,cantDecimales=4,alfabetoEnt=alfabetoEnt,alfabetoSal=alfabetoSal,mostrar=True)
    print("\n\n")

def ej8():
    auxMostrarProbsSalida("abcacaabbcacaabcacaaabcaca","01010110011001000100010011")
    print("\n\n")
    auxMostrarProbsSalida("1101011001101010010101010100011111","1001111111100011101101010111110110")
    print("\n\n")
    auxMostrarProbsSalida("110101100110101100110101100111110011","110021102110022010220121122100112011")
    print("\n\n")
    
def ej9():
    auxMostrarProbsPosteriori("abcacaabbcacaabcacaaabcaca","01010110011001000100010011")
    auxMostrarProbsPosteriori("1101011001101010010101010100011111","1001111111100011101101010111110110")
    auxMostrarProbsPosteriori("110101100110101100110101100111110011","110021102110022010220121122100112011")
    print("\n-------  ------- -------  ------- -------  ------- -------  -------  -------  -------  -------  ------- -------  ------- \n\n\n")
    
    auxMostrarProbsSimultaneas("abcacaabbcacaabcacaaabcaca","01010110011001000100010011")
    auxMostrarProbsSimultaneas("1101011001101010010101010100011111","1001111111100011101101010111110110")
    auxMostrarProbsSimultaneas("110101100110101100110101100111110011","110021102110022010220121122100112011")
    
'''
    11. Desarrollar una función en Python que reciba como parámetros: una lista con las
    probabilidades a priori y la matriz de probabilidades condicionales del canal, y retorne una
    lista con las entropías a posteriori. '''

def generarEntropiasPosteriori(probabilidadesPriori,matriz):
    matProbsPost = generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matriz)
    r = len(matProbsPost)
    s = len(matProbsPost[0])
    entropiasPost = [0] * s
    
    for j in range(s):
        for i in range(r):
            prob = matProbsPost[i][j]
            if (prob > 0):
                entropiasPost[j] += prob * math.log2(1/prob)
            
    return entropiasPost
                
def ej10():
    print("C1: ",generarEntropiasPosteriori([2/5,3/5],[[3/5,2/5],[1/3,2/3]]),"\n")
    print("C2: ",generarEntropiasPosteriori([3/4,1/4],[[2/3,1/3],[1/10,9/10]]),"\n")
    
def auxMostrarEntropias(entrada,salida):
    probsPriori = generarProbabilidades(entrada)
    matrizCanal = generarMatrizProbabilidadesCondicionales(entrada,salida)
    entropiaPriori = obtenerEntropia(probsPriori,2)
    entropiaPosteriori = generarEntropiasPosteriori(probsPriori,matrizCanal)
    
    print("Entropia A-Priori H(A): ",entropiaPriori)
    print("Entropia A-Posteriori H(A/bj): ",entropiaPosteriori)
    print("\n\n")
    
def auxMostrarEntropiasPeroConMatrizYProbs(probsPriori,matriz):
    entropiaPriori = obtenerEntropia(probsPriori,2)
    entropiaPosteriori = generarEntropiasPosteriori(probsPriori,matriz)

    print(f"Entropia A-Priori H(A): {entropiaPriori:.4f}")
    print("Entropia A-Posteriori H(A/bj): ",end="")
    imprimirLista(entropiaPosteriori,cantDecimales=4)
    print("\n\n")
    
def ej12():
    print("Ej1: ")
    auxMostrarEntropias("abcacaabbcacaabcacaaabcaca","01010110011001000100010011")

    print("Ej3 Canal1:")
    auxMostrarEntropias("1101011001101010010101010100011111","1001111111100011101101010111110110")
    print("Ej3 Canal2:")
    auxMostrarEntropias("110101100110101100110101100111110011","110021102110022010220121122100112011")

    auxMostrarEntropiasPeroConMatrizYProbs([0.3, 0.3, 0.4],[[0.4,0.4,0.2],[0.3,0.2,0.5],[0.3,0.4,0.3]])
    
    
def ej13():
    print(" --- Ejericio 13 --- \n")
    probsPriori1=[0.14,0.52,0.34]
    mat1=[[0.5,0.3,0.2], [0.0,0.4,0.6], [0.2,0.8,0.0]]
    probsPriori2=[0.25,0.25,0.5]
    mat2=[[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.0, 0.5], [0.5, 0.0, 0.5, 0.0]]
    probsPriori3=[0.12, 0.24, 0.14, 0.5]
    mat3=[[0.25,0.15,0.3,0.3], [0.23,0.27,0.25,0.25], [0.1,0.4,0.25,0.25], [0.34,0.26,0.2,0.2]]

    print("Canal 1: ")
    auxMostrarEntropiasPeroConMatrizYProbs(probsPriori1,mat1)

    print("Canal 2: ")
    auxMostrarEntropiasPeroConMatrizYProbs(probsPriori2,mat2)

    print("Canal 3: ")
    auxMostrarEntropiasPeroConMatrizYProbs(probsPriori3,mat3)
    

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
    # ej3()
    # ej8()
    # ej9()
    # ej10()
    # ej12()
    ej13()

main()