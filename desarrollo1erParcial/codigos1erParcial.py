import math
import random


#                       MEMORIA NULA

def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

def obtenerEntropia(probabilidades, informaciones):
    suma = 0
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

# generar una fuente (alfabeto y probabilidades) de memoria nula a partir de una cadena
def generarFuente(cadena):
    alfabeto = []
    probabilidades = []
    for i in cadena:
        if (i not in alfabeto):
            alfabeto.append(i)
            probabilidades.append(0)
        probabilidades[alfabeto.index(i)] += 1
    probabilidades = [prob / len(cadena) for prob in probabilidades]

    return alfabeto, probabilidades

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

def obtenerEntropiaBinaria(w): # en realidad es omega, no w, pero bueno
    probs = [w,1-w]
    infs = generarListaInformacion(probs)
    print("\nProbs =",probs,"\nInfs= ",infs)
    return obtenerEntropia(probs, infs) # tmb se podia hacer return w*math.log2(1/w) + (1-w)*math.log2(1/(1-w))

def generarExtensionFuente(alfabeto, probabilidades, n):
    alfabetoExtendido = []
    probabilidadesExtendido = []
    posiciones = [0] * n
    carry = 0
    q = len(alfabeto)

    while (carry != 1):
        # construir la palabra extendida y la probabilidad
        palabra = ""
        prob = 1
        for pos in posiciones:
            palabra += alfabeto[pos]
            prob *= probabilidades[pos]

        alfabetoExtendido.append(palabra)
        probabilidadesExtendido.append(prob)

        # avanzar la posición
        if (posiciones[n-1] + 1 < q):
            posiciones[n-1] += 1 
        else:
            posiciones[n-1] = 0
            carry = 1
            i = n - 2 
            while (carry == 1 and i >= 0):
                if (posiciones[i] + 1 < q):
                    posiciones[i] += 1
                    carry = 0
                else:
                    posiciones[i] = 0
                    carry = 1
                    i -= 1
            
    return alfabetoExtendido, probabilidadesExtendido





#                       MEMORIA NO NULA (MARKOV DE ORDEN 1)

def cumpleTolerancia(vec1,vec2, tolerancia = 0.001):
    vec3 = [abs(x - y) for x,y in zip(vec1,vec2)]
    return max(vec3) < tolerancia


def imprimirMatriz(mat):
    for fila in mat: 
        for elemento in fila:
            print(f"{elemento:.4f}",end="\t\t")
        print()
    print()
    
def productoMatricial(matriz, vector):
    n = len(matriz)
    vecAux = [0] * n
    for i in range(n):
        for j in range(n):
            vecAux[i] += matriz[i][j] * vector[j]
    return vecAux

def generarVectorEstacionario(matriz, tolerancia = 0.001):
    n = len(matriz)
    vec = [1/n] * n
    cumpleTol = False
    while(not cumpleTol):
        vecAux = productoMatricial(matriz,vec)
        cumpleTol = cumpleTolerancia(vec,vecAux,tolerancia)
        vec = vecAux
    return vec
    
def obtenerEntropiaMarkoviana(matrizTransicion, vectorEstacionario):
    suma = 0
    n = len(vectorEstacionario)
    for k in range(0,n):
        aux = 0
        for i in range(0,n):
            if (matrizTransicion[i][k] != 0):
                aux += matrizTransicion[i][k] * math.log2(1/matrizTransicion[i][k])
        suma += vectorEstacionario[k] * aux
    return suma

def generarFuenteMarkoviana(cadena):
    alfabeto = []
    matriz = []
    # genero alfabeto
    for i in range(0,len(cadena)):
        if (cadena[i] not in alfabeto):
            alfabeto.append(cadena[i])
    n = len(alfabeto)
    matriz = [[0] * n for _ in range(n)]

    # acumulo apariciones
    for i in range(1,len(cadena)):
        matriz[alfabeto.index(cadena[i])][alfabeto.index(cadena[i-1])] += 1

    # normalizo
    for k in range(n):
        suma = 0
        for i in range(n):
            suma += matriz[i][k]
        if (suma>0):
            for i in range(n):
                matriz[i][k] /= suma
        else:
            for i in range(n):
                matriz[i][k] = 0

    return alfabeto, matriz

def devolverPrimerSimbolo(alfabeto,vec):
    r = random.random()
    probAcumulada = 0.0
    for i in range(0,len(vec)):
        if (r < probAcumulada + vec[i]):
            return alfabeto[i]
        else:
            probAcumulada += vec[i]

def devolverSimbolo(alfabeto, matriz,j):
    r = random.random()
    probAcumulada = 0.0
    for i in range(0,len(matriz)):
        if (r < probAcumulada + matriz[i][j]):
            return alfabeto[i]
        else:
            probAcumulada += matriz[i][j]

def generarCadena(alfabeto, matriz, n):
    cadena = ""
    cadena += devolverPrimerSimbolo(alfabeto, generarVectorEstacionario(matriz))
    for i in range(1,n):
        c = devolverSimbolo(alfabeto,matriz,alfabeto.index(cadena[i-1]))
        cadena += c
    return cadena

def esNula(mat, tolerancia = 0.001): # es nula o no es nula, esa es la cuestión
    return cumpleTolerancia([max(fila) for fila in mat],[min(fila) for fila in mat],tolerancia)





#                       PROPIEDADES DE LOS CÓDIGOS

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

def esInstantaneo(palabrasCodigo,mostrarPasosUnivoco = False):
    aux = esUnivoco(palabrasCodigo,mostrarPasosUnivoco) # si el alfabeto código no es univoco entonces no es instantáneo
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

def esUnivoco(palabrasCodigo,mostrarPasos = False):
    if (not esNoSingular(palabrasCodigo)):
        return False
    # algoritmo de Sardinas-Patterson
    conjSuf = [] # lista de conjuntos/sets S=[S1, S2, .., Sn] siendo Si={el1,el2,..,eln}
    conjSuf.append(set(palabrasCodigo))
    if (mostrarPasos):
        print("S0 = ",conjSuf[0])
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
        if (mostrarPasos):
            print(f"S{k} = ",conjSuf[k])
        
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
                
     
                
def generarAlfabetoCodigo(palabrasCodigo):
    alfabetoCodigo = []
    for palabra in palabrasCodigo:
        for caracter in palabra:
            if caracter not in alfabetoCodigo:
                alfabetoCodigo.append(caracter)
    return alfabetoCodigo

def generarLongitudes(palabrasCodigo):
    return [len(palabra) for palabra in palabrasCodigo]

def sumatoriaKraft(palabrasCodigo):
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
    longitudes = generarLongitudes(palabrasCodigo)
    suma = 0
    r = len(alfabetoCodigo)
    for long in longitudes:
        suma += r ** -long
    return suma

def cumpleKraft(palabrasCodigo):
    return sumatoriaKraft(palabrasCodigo) <= 1

def obtenerLongitudMedia(palabrasCodigo, probabilidades):
    return sum([prob * len(palabra) for palabra,prob in zip(palabrasCodigo, probabilidades)])

def esCompacto(palabrasCodigo, probabilidades):
    aux = esUnivoco(palabrasCodigo)
    r = len(generarAlfabetoCodigo(palabrasCodigo))
    longs = generarLongitudes(palabrasCodigo)
    infs = generarListaInformacion(probabilidades,r)
    i = 0
    while (aux and i < len(palabrasCodigo)):
        aux = longs[i] <= math.ceil(infs[i])
        i += 1
    return aux


def devolverPalabra(palabrasCodigo,probabilidades):
    r = random.random()
    probAcumulada = 0.0
    i = 0
    while (r >= probAcumulada + probabilidades[i]):
        probAcumulada += probabilidades[i]
        i += 1
    return palabrasCodigo[i]

def generarCadenaPalabras(palabrasCodigo,probabilidades,n):
    cad = ""
    for i in range(n):
        cad += devolverPalabra(palabrasCodigo,probabilidades)
        cad += " "
    return cad

def clasificarCodigo(palabrasCodigo):
    if (esInstantaneo(palabrasCodigo,True)):
        print("Instantáneo")
    elif (esUnivoco(palabrasCodigo)):
        print("Unívoco/Unívocamente Decodificable")
    elif(esNoSingular(palabrasCodigo)):
        print("No Singular")
    else:
        print("Código Bloque")


'''
1) Para cada uno de los siguientes mensajes, emitidos por fuentes de información:

a) Determinar el alfabeto y las probabilidades de sus símbolos
b) Obtener la matriz de transición de la fuente
c) Estimar si se trata de una fuente de memoria nula o no nula
d) Calcular la entropía de la fuente
e) Si es una fuente de memoria nula, generar la extensión de orden 2 y calcular su entropía a partir de sus probabilidades
f) Si es una fuente con memoria, obtener el vector estacionario 
'''
def ej1(msj):

    # a)
    alfabeto, probabilidades = generarFuente(msj)
    print("Alfabeto: ",alfabeto)
    print("Probabilidades: ",probabilidades, "\n")

    # b)    
    aux, matriz = generarFuenteMarkoviana(msj)
    print("Matriz de Transición: ")
    imprimirMatriz(matriz)
    print()
    
    # c), d), e)
    if (esNula(matriz)):
        print("Fuente de Memoria nula \n")
        print("Entropía: ",obtenerEntropia(probabilidades,generarListaInformacion(probabilidades,2)), "bits")
        alfabetoExt, probabilidadesExt = generarExtensionFuente(alfabeto,probabilidades,2)
        entrExt = obtenerEntropia(probabilidadesExt,generarListaInformacion(probabilidadesExt,2))
        print("Extensión de Orden 2")
        print("Alfabeto: ",alfabetoExt)
        print("Probabilidades: ",probabilidadesExt)
        print("Entropía: ",entrExt)
    else: 
        print("Fuente de Memoria No nula\n")   
        vectorEstacionario = generarVectorEstacionario(matriz)
        print("Entropía: ",obtenerEntropiaMarkoviana(matriz,vectorEstacionario), "bits")
        print("Vector Estacionario: ",vectorEstacionario)

    

'''
2) Para cada uno de los siguientes códigos:
a) Identificar el alfabeto código
b) Calcular la entropía de la fuente y la longitud media del código
c) Comprobar si la codificación cumple la inecuación de Kraft-McMillan
d) Clasificarlo de acuerdo a sus propiedades
e) Determinar si se trata de un código compacto
f) En caso de haber utilizado el algoritmo de Sardinas-Patterson, informar los resultados obtenidos en cada paso        
'''
    
def ej2(palabrasCodigo, probabilidades):
    # a)
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
    print("Alfabeto Código: ",alfabetoCodigo)
    
    # b)
    entropia = obtenerEntropia(probabilidades, generarListaInformacion(probabilidades,len(alfabetoCodigo)))
    longitudMedia = obtenerLongitudMedia(palabrasCodigo,probabilidades)
    print("Entropía: ",entropia)
    print("Longitud Media: ",longitudMedia)
    
    # c)
    kraft = sumatoriaKraft(palabrasCodigo)
    print("Kraft: ",kraft)
    if (kraft <= 1.0):
        print("Cumple la Inecuación de Kraft-Macmillan")
    else:
        print("NO Cumple la Inecuación de Kraft-Macmillan")
    
    # d) y f)
    clasificarCodigo(palabrasCodigo)
    
    # e)
    if (esCompacto(palabrasCodigo,probabilidades)):
        print("El Código es Compacto")
    else:
        print("El Código NO es Compacto")    
    
    
    
    
    
    


def main():
    print(" EJERCICIO 1")

    print(" MENSAJE 1\n")
    ej1(";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;")

    print("\n\n MENSAJE 2\n")
    ej1("-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//") 




    print("\n\n\n EJERCICIO 2\n")

    print(" CÓDIGO 1\n")
    ej2(["/+","*","+-","-","*/"],[0.15,0.25,0.05,0.45,0.10])

    print("\n\n CÓDIGO 2\n")
    ej2(["(]","]","[)",")","(["],[0.15,0.25,0.05,0.45,0.10])
    
    
main()