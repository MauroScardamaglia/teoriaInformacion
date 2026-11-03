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

def obtenerRuido(probabilidadesPriori,matrizCanal): # H(A/B)
    s = len(matrizCanal[0])
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    entropiasPost = generarEntropiasPosteriori(probabilidadesPriori,matrizCanal) 

    ruido = 0
    for j in range(s):
        ruido += probsSalida[j] * entropiasPost[j]
    return ruido


def obtenerPerdida(probabilidadesPriori,matrizCanal): # H(B/A)
    r = len(matrizCanal)
    s = len(matrizCanal[0])


    # obtengo H(B/ai) (entropiaCondicionalSalida)

    entropiasCondicionalSalida = [0] * r    
    for i in range(r):
        for j in range(s):
            prob = matrizCanal[i][j]
            if (prob > 0):
                entropiasCondicionalSalida[i] += prob * math.log2(1/prob)

    # -----

    perdida = 0
    for i in range(r):
        perdida += probabilidadesPriori[i] * entropiasCondicionalSalida[i]

    return perdida


def obtenerEntropiaAfin(probabilidadesPriori,matrizCanal): # H(A,B) # entropia afín <-> entropía conjunta
    entropiaPriori = obtenerEntropia(probabilidadesPriori,2)
    entropiaSalida = obtenerEntropia(generarProbabilidadesSalida(probabilidadesPriori,matrizCanal),2)
    informacionMutua = obtenerInformacionMutua(probabilidadesPriori,matrizCanal)
    return entropiaPriori + entropiaSalida - informacionMutua


def obtenerInformacionMutua(probabilidadesPriori,matrizCanal): # I(A,B)
    entropiaPriori = obtenerEntropia(probabilidadesPriori,2)
    ruido = obtenerRuido(probabilidadesPriori,matrizCanal)
    return entropiaPriori - ruido

def auxEj16(probabilidadesPriori,matrizCanal):
    print(f"a) Entropía a Priori H(A) = {obtenerEntropia(probabilidadesPriori,2):.4f}")
    print(f"b) Entropía de la Salida H(B) = {obtenerEntropia(generarProbabilidadesSalida(probabilidadesPriori,matrizCanal),2):.4f}")
    print(f"c) Equivocación de A respecto a B / Ruido H(A/B) = {obtenerRuido(probabilidadesPriori,matrizCanal):.4f}")
    print(f"d) Pérdida H(B/A) = {obtenerPerdida(probabilidadesPriori,matrizCanal):.4f}")
    print(f"e) Entropía Afín/Conjunta H(A,B) = {obtenerEntropiaAfin(probabilidadesPriori,matrizCanal):.4f}")
    print(f"f) Información Mutua I(A,B) = {obtenerInformacionMutua(probabilidadesPriori,matrizCanal):.4f}")
    print("\n\n")

def ej16():
    print("--- Ejercicio 13 ---\n")
    probsEj13_1=[0.14,0.52,0.34]
    matEj13_1=[[0.5,0.3,0.2], [0.0,0.4,0.6], [0.2,0.8,0.0]]
    probsEj13_2=[0.25,0.25,0.5]
    matEj13_2=[[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.0, 0.5], [0.5, 0.0, 0.5, 0.0]]
    probsEj13_3=[0.12, 0.24, 0.14, 0.5]
    matEj13_3=[[0.25,0.15,0.3,0.3], [0.23,0.27,0.25,0.25], [0.1,0.4,0.25,0.25], [0.34,0.26,0.2,0.2]]

    probs = [probsEj13_1,probsEj13_2,probsEj13_3]
    mats = [matEj13_1,matEj13_2,matEj13_3]

    for prob,mat in zip(probs,mats):
        auxEj16(prob,mat)

    print("--- Ejercicio 14 --- \n")
    probsEj14_1=[0.7,0.3]
    matEj14_1=[[0.7,0.3],[0.4,0.6]]

    probsEj14_2=[0.5,0.5]
    matEj14_2 = [[0.3,0.3,0.4],[0.3,0.3,0.4]]

    probsEj14_3=[0.25,0.5,0.25]
    matEj14_3 = [[1,0,0,0],[0,0.5,0.5,0],[0,0,0,1]]

    probsEj14_4=[0.25,0.25,0.25,0.25]
    matEj14_4 = [[1,0,0],[0,1,0],[0,1,0],[0,0,1]]

    probs = [probsEj14_1,probsEj14_2,probsEj14_3,probsEj14_4]
    mats = [matEj14_1,matEj14_2,matEj14_3,matEj14_4]

    for prob,mat in zip(probs,mats):
        auxEj16(prob,mat)

'''
    18. Realizar funciones booleanas en Python que reciban como parámetro la matriz de un canal
    y verifiquen si se trata de:
    a. Un canal sin ruido
    b. Un canal determinante '''

def esCanalSinRuido(matrizCanal):
    aux = True
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    j = 0
    
    while (aux and j<s):
        i = 0
        cantEncontrado = 0
        while (cantEncontrado <= 1 and i<r):
            if (matrizCanal[i][j] > 0):
                cantEncontrado += 1
            i += 1
        aux = cantEncontrado <= 1
        j += 1
        
    return aux

    

def esCanalDeterminante(matrizCanal):
    aux = True
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    i = 0
    
    while (aux and i<r):
        j = 0
        cantEncontrado = 0
        while (cantEncontrado <= 1 and j<s):
            if (matrizCanal[i][j] > 0):
                cantEncontrado += 1
            j += 1
        aux = cantEncontrado <= 1
        i += 1

    return aux

def auxComprobarFuncionamientoCanalesRuidoODeterminante(): # cortito el título
    canales = [ # si tengo una lista de matrices, sería como un cubo? (claro que no regular, onda no tienen las mismas dimensiones todas las matrices)
    [[0,1,0],[0,0,1],[0,1,0],[1,0,0]],
    [[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]],
    [[0.3,0.5,0.2],[0.2,0.3,0.5],[0.5,0.2,0.3]],
    [[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]
    ]
    
    for matriz in canales:
        print("Matriz:")
        imprimirMatriz(matriz)
        print()
        if (not esCanalSinRuido(matriz)):
            print("No ",end="")
        print("Es canal Sin Ruido")
        
        if (not esCanalDeterminante(matriz)):
            print("No ",end="")
        print("Es canal Determinante")
        print("\n\n")

'''
    20. Implementar una función en Python que reciba como parámetros las matrices de dos
    canales y genere la matriz del canal compuesto por los canales en serie. '''

def generarMatrizCompuesta(matrizA,matrizB): # productoMatricial
    # productoMatricial
    r = len(matrizA)
    s = len(matrizB)
    
    matrizC = [ [0] * (s-1) for _ in range(r)]
    
    for i in range(r):
        for j in range(s-1):
            # elemento actual de la nueva matriz
            aux = 0
            for k in range(s):
                aux += matrizA[i][k]* matrizB[k][j]
            matrizC[i][j] = aux
        
    return matrizC
            


'''
    22. Desarrollar funciones en Python que reciban como parámetros: la matriz de un canal y los
    índices de dos columnas, y realicen lo siguiente:
    a. Verificar si las columnas se pueden combinar en una reducción suficiente
    b. Generar la matriz del canal determinante necesario para combinar las columnas '''

def columnasSonCombLineal(matrizCanal,j1,j2):
    aux = True
    r = len(matrizCanal)
    i = 1
    proporcion = matrizCanal[i][j2] / matrizCanal[i][j1] # factor que multiplica a la primera columna para ser igual a la segunda (el orden es arbitrario)
    while (aux and i<r):
        aux = (matrizCanal[i][j1] * proporcion) == matrizCanal[i][j2]
        i += 1
    return aux
    
def generarMatrizDeterminante(matrizCanal,j1,j2):
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    matrizDeterminante = [[0] * (s-1) for _ in range(r)]
    if (j2<j1):
        aux = j2
        j2 = j1
        j1 = aux
    k = 0
    for i in range(s):
        if (i == j2):
            matrizDeterminante[i][j1] = 1
        else:
            matrizDeterminante[i][k] = 1
            k += 1
            
    return matrizDeterminante


'''
    23. Codificar una función en Python que reciba como parámetro la matriz de un canal y,
    utilizando las funciones de los ejercicios 20 y 22, realice todas las reducciones suficientes
    posibles y devuelva la matriz del canal reducido '''

def esReducible(matriz): # devuelve las columnas j1 y j2 (que son CL), en caso de no ser reducible devuelve (-1,-1)
    # comprobación de reducción posible
        s = len(matriz[0])
        j1 = 0
        while (not aux and j1 < s):
            j2 = j1 + 1
            while(not aux and j2 < s):
                aux = columnasSonCombLineal(matriz,j1,j2)
                j2 += 1
            j1 += 1
            
        if (aux):
            j1 -= 1
            j2 -= 1
            return j1, j2
        else:
            return -1, -1
        

def reducirMatriz(matrizCanal):
    matriz = matrizCanal
    while (True):
        j1, j2 = esReducible(matriz)
        if (j1 == -1):
            break
        matDet = generarMatrizDeterminante(matriz,j1,j2)
        matriz = generarMatrizCompuesta(matriz,matDet)
        
    return matriz
    
    
    
'''
    25. Implementar funciones en Python que reciban como parámetro la matriz de un canal y
    resuelvan lo siguiente:

    a. Verificar si se trata de un canal uniforme (no entra en el parcial) '''

def esCanalUniforme(matrizCanal):
    r = len(matrizCanal)
    s = len(matrizCanal[0])

    # verifico que todas las filas sean permutaciones entre sí
    elementos = matrizCanal[0]
    i = 0
    aux = True
    while(i<r):
        j = 0
        while(aux and j<s):
            aux = matrizCanal[i][j] in elementos
            j += 1
        i += 1

    # verifico que sean permutaciones distintas (en caso contrario las columnas no suman 1 y... 
    # arbitrariamente, eligo el primer elemento de la primera fila, y verifico que el j donde se ubica sea distinto en todas las filas
    posiciones = [-1] * r
    valor = matrizCanal[0][0]
    i = 0
    while (aux and i < r):
        posiciones[i] = matrizCanal[i].index(valor)
        k = 0
        while (aux and k < i):
            aux = posiciones[i] not in posiciones[0:i]
            k += 1
        i += 1

    return aux

def auxProbarEsCanalUniforme():
    canal = [[0.3,0.5,0.2],[0.2,0.3,0.5],[0.5,0.2,0.3]] # -> true 
#    canal = [[0.3,0.5,0.2],[0.2,0.3,0.5],[0.2,0.3,0.5]] #[0.5,0.2,0.3]] # -> false
    imprimirMatriz(canal,cantDecimales=4)
    print("Es uniforme? -> ",esCanalUniforme(canal))

    
'''
    b. Calcular su capacidad en los siguientes casos:
    i. Canal determinante
    ii. Canal sin ruido
    iii. Canal uniforme (no entra en el parcial) '''

def capacidadCanalDeterminante(matrizCanal):
    return math.log2( len(matrizCanal[0]) ) # log2(s) , s= cantSalidas

def capacidadCanalSinRuido(matrizCanal):
    return math.log2( len(matrizCanal) ) # log2(r) , r= cantidadEntradas

def capacidadCanalUniforme(matrizCanal): # no entra en el parcial
    return math.log2(len(matrizCanal[0])) - obtenerEntropia(matrizCanal[0]) # log2(s) - H(fila)

'''
    26. Realizar una función en Python que reciba como parámetros: la matriz de un canal binario
    y un valor de paso, y estime la capacidad del canal mediante el cálculo de la información
    mutua para un conjunto de probabilidades a priori distribuidas uniformemente según el
    paso especificado. La función debe retornar el valor de capacidad estimado, junto con su
    probabilidad asociada. '''


def capacidadCanalBinario(matrizCanal,paso): # Binario -> r = s = 2 (no necesariamente simétrico)
    p = 0 # o pInicial = paso ?? 
    infoMaxima = -1
    pMaximo = -1

    while (p <=1):
        probsPriori = [p,1-p] # [p, compl(p)]
        infMutua = obtenerInformacionMutua(probsPriori,matrizCanal)
        if (infMutua > infoMaxima):
            infoMaxima = infMutua
            pMaximo = p
        p += paso

    capacidad = infoMaxima # completamente innecesario, pero queda más claro el concepto
    return capacidad, pMaximo

    
# 27. Para cada uno de los siguientes canales binarios, determinar su capacidad y la distribución
# de probabilidades a priori que maximiza la información mutua:

def ej27():
    canal1 = [[0.6,0.4],[0.2,0.8]]
    canal2 = [[0.25,0.75],[0.9,0.1]]
    canal3 = [[0.51,0.49],[0.72,0.28]]
    canal4 = [[0.77,0.23],[0.2,0.8]]

    canales = [canal1,canal2,canal3,canal4]
    paso = 0.0001 # 100 iteraciones (o 101?)

    for i,canal in zip(range(len(canales)),canales):
        print(f"Canal {i}")
        capacidad, pMaximo = capacidadCanalBinario(canal,paso)
        print(f"La información mutua máxima (Capacidad) es C = {capacidad:.4f}")
        print(f"La distribución de Probabilidades a Priori correspondiente es: [{pMaximo:.4f},{(1-pMaximo):.4f}]")
        print("\n\n")


'''
    30. Desarrollar una función en Python que reciba como parámetros: una lista con
    probabilidades a priori y la matriz de un canal, y calcule la probabilidad de error utilizando
    la regla de decisión de máxima posibilidad. '''

def obtenerProbabilidadError(probabilidadesPriori,matrizCanal):
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    matProbsPost = generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matrizCanal)
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    probsError = [0] * s
    
    for j in range(s):
        # encuentro el a* (el i de esa columna con la mayor probabilidad)
        aEstrella = -1 # por poner un valor predeterminado imposible
        valMaximo = 0
        for i in range(r):
            if (matProbsPost[i][j] > valMaximo):
                valMaximo = matProbsPost[i][j]
                aEstrella = i

        # obtengo la probabilidad de Error de la columna actual P(E/bj)
        probsError[j] = 1 - valMaximo

    probabilidadError = 0
    for j in range(s):
        probabilidadError += probsError[j] * probsSalida[j]

    return probabilidadError

# ---------------------- MAIN ----------------------

def main():
    print("hallo, ich bin Mauro's Geist \n")
    # ej3()
    # ej8()
    # ej9()
    # ej10()
    # ej12()
    # ej13()
    # ej16()
    # auxComprobarFuncionamientoCanalesRuidoODeterminante()
    # ej27()
    auxProbarEsCanalUniforme()

main()