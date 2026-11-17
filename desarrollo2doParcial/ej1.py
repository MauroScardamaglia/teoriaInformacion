import math
import random

# software necesario para resolver el 2do Parcial



def imprimirLista(lista,cantDecimales=4):
    n = len(lista)
    print("[",end="")
    for i in range(n-1):
        print(f"{lista[i]:.{cantDecimales}f}, ",end="")
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


# ------------------- TEOREMA DE SHANNON ------------------- 

def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

def obtenerEntropia(probabilidades, r):
    suma = 0
    informaciones = generarListaInformacion(probabilidades,r)
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

def generarExtensionProbabilidades(probabilidades,n): # solo para extender probabilidades, sin importar alfabeto
    probabilidadesExt = []
    posiciones = [0] * n
    carry = 0
    q = len(probabilidades)

    while(carry != 1):
        prob = 1
        for pos in posiciones:
            prob *= probabilidades[pos]
        
        probabilidadesExt.append(prob)
        
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
    
    return probabilidadesExt

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


def generarAlfabetoCodigo(palabrasCodigo):
    alfabetoCodigo = []
    for palabra in palabrasCodigo:
        for caracter in palabra:
            if caracter not in alfabetoCodigo:
                alfabetoCodigo.append(caracter)
    return alfabetoCodigo

def obtenerLongitudMedia(palabrasCodigo, probabilidades):
    return sum([prob * len(palabra) for palabra,prob in zip(palabrasCodigo, probabilidades)])

# se pasa el código original
def cumpleShannon(palabrasCodigo, probabilidades, n, mostrar = False):
# Las probabilidades que recibo son las de la fuente original, q probabilidades
#
# Tengo que pasar las palabras código para la extensión
# y calcular el código acorde antes de llamar a la función
# el dolor de huevos está en calcular un código eficiente (que es complejo por su largo)
#
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
#    q = len(probabilidades)
#    aux, probabilidadesExt = generarExtensionFuente(["a"]*q,probabilidades,n)
    probabilidadesExt = generarExtensionProbabilidades(probabilidades,n)
    entropia = obtenerEntropia(probabilidades, len(alfabetoCodigo))

    longMedia = obtenerLongitudMedia(palabrasCodigo,probabilidadesExt) # Ln
    cotaInf = entropia
    cotaSup = entropia + 1/n

    if (mostrar):
        print("Hr(S) = ",cotaInf)
        print("Ln/n = ",longMedia/n)
        print("Hr(S) + 1/n = ",cotaSup)

    return (cotaInf <= longMedia/n) and (longMedia/n < cotaSup)

def obtenerRendimientoCodigo(palabrasCodigo,probabilidades): # retorna rendimiento, redundancia (η, R)
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
    r = len(alfabetoCodigo)
    entropia = obtenerEntropia(probabilidades, r)
    longMedia = obtenerLongitudMedia(palabrasCodigo,probabilidades)
    return entropia / longMedia , 1 - (entropia / longMedia)

def obtenerDistanciaHamming(cad1,cad2,mostrar=False):
    if (mostrar):
        print()
        print(cad1)
        print(cad2)
        print()

    if (len(cad1) != len(cad2)):
        return -1
    else:
        d = 0
        for x,y in zip(cad1,cad2):
            if (x != y):
                d += 1
        return d

def obtenerDistanciaHammingCodigo(codigo):
    dMin = 9999

    for i in range(len(codigo)):
        for j in range(i+1,len(codigo)):
            aux = obtenerDistanciaHamming(codigo[i],codigo[j])
            if (aux < dMin):
                dMin = aux

    alpha = dMin - 1
    beta = math.floor((dMin - 1)/2)
    return dMin, alpha, beta

def verificarParidad(msj): # recibe una lista con caracteres '0' o '1'
    return msj.count('1') % 2 == 0 # si sumamos el bit de paridad a la cantidad de 1's, lo que hace el bit es hacer la cantidad par (si era impar suma 1, si era par suma 0)

def darRedundanciaCaracter(c,mostrar = False): # retorna String
    if (mostrar): print("'",c,"'")
    cad = ord(c)
    if (mostrar): print(cad)

    cad = bin(cad)
    cad = cad[2:] # quito el "0b"
    if (mostrar): print(cad)
    # bin devuelve un string "0b10101010" siempre empieza en 1
    l = len(cad)
    if (l<7):
        aux = ""
        for k in range(7-l):
            aux += "0"
        cad = aux + cad # relleno con 0's para que sean 7 caracteres

    cad += str(cad.count('1') % 2)
    if (mostrar): print(cad)
    return cad

def imprimirMensajRedund(mensaje):
    for x in mensaje[0][:-1]:
        print(x,end="\t")
    print("| ",mensaje[0][-1])

    for x in mensaje[0]:
        print("--------",end="")
    print()

    for x in mensaje[1:]:
        for y in x[:-1]:
            print(y,end="\t")
        print("| ",x[-1])

def generarMensajeConParidades(cadena,mostrar = False):
    if (mostrar): print(cadena,"\n")
    mat = [[0] * 8]
#    if (mostrar): imprimirMensajRedund(mat)

    for c in cadena:
        filaBin = list(darRedundanciaCaracter(c)) # casteo de string a lista de caracteres
        mat.append(filaBin)
    if (mostrar):
        imprimirMensajRedund(mat)
        print("\n\n")
    
    for j in range(0,8):
        colBin = [fila[j] for fila in mat[1:]]
        vrc = str(colBin.count('1') % 2) # vrc queda conformado como '1' o '0'
        mat[0][j] = vrc
    if (mostrar): imprimirMensajRedund(mat)
    
    return mat

def corregirMensaje(msj): # devuelve el mensaje original, si no había errores o se pueden corregir; caso contrario devuelve algo gracioso xD
    n = len(msj)
    m = len(msj[0])
    mensaje=[]
    for i in range(n):
        fila = []
        for j in range(m):
            fila.append(msj[i][j])
        mensaje.append(fila)
            
    # almacenan i y j's
    filasConErrores = [] 
    colConErrores = [] 
    

    # ANALIZAR PRIMERO BIT DE PARIDAD CRUZADA
    # al final decidí verificar si el error está en el bit de paridad cruzado al final de la función
    
    
    i = 0
    while (len(filasConErrores) <=1 and i < n):
        if (not verificarParidad(mensaje[i])):
            filasConErrores.append(i)
        i += 1
            
    if (len(filasConErrores) <=1):
        j = 0
        while (len(colConErrores) <=1 and j < m):
            col = [fila[j] for fila in mensaje]
            if (not verificarParidad(col)):
                colConErrores.append(j)
            j += 1
    
    if (len(filasConErrores) == len(colConErrores) == 0): # mensaje sin errores
        return mensaje
    elif (len(filasConErrores) > 1 or len(colConErrores) > 1): # errores > β
        return [["?"] * m] * n
    else: # 1 error solo (β = 1)
        i = filasConErrores[0]
        j = colConErrores[0]
        
        if (i == n-1 and j == m-1): # el error está en el bit de paridad cruzada, no se puede asumir la integridad del mensaje
            return [["?"] * m] * n
        
        if (mensaje[i][j] == "0"):
            mensaje[i][j] = "1"
        else:
            mensaje[i][j] = "0"
        return mensaje




# ------------------- COMPRESIÓN ------------------- 

def generarCodigoHuffman(probabilidades):
    items = [[p,""] for p in probabilidades]
    huffmanRecursivo(sorted(items,reverse=False))
    return [palCodigo for _ , palCodigo in items]

def huffmanRecursivo(items): # recibe una lista con el formato [prob, "codigo"] ordenado de forma ascendente
    # devuelve la misma lista (mismo tamaño) pero con los códigos ya "configurados"
    
    # a = b.copy() <-> a = b[:]
    # ámbas son copias superficiales (es lo que quiero)
    
    # casos bases
    if (len(items) == 1):
        a = items[0]
        a[1] = "0"
    elif (len(items) == 2):
        a = items[0]
        b = items[1]
        a[1] = "1"
        b[1] = "0"
    else:
        a = items[0]
        b = items[1]
        itemsReducido = items[2:]
        aux = [a[0]+b[0], ""] # aux mantiene la referencia al bloque armado
        itemsReducido.append(aux) # agrego el bloque
        itemsReducido = sorted(itemsReducido,reverse=False) # ordeno
        huffmanRecursivo(itemsReducido)
        
        #arbitrariamente al más probable le asigno 0, y viceversa
        # estas 2 líneas son fundamentales, son las que construyen el código
        a[1] = aux[1] + "1"
        b[1] = aux[1] + "0"
        

def generarCodigoShannonFano(probabilidades):
    items = [[p,""] for p in probabilidades]
    shannonFanoRecursivo(sorted(items,reverse=True))
    return [palCodigo for _ , palCodigo in items]

def shannonFanoRecursivo(items):
    if (len(items) > 1):
        total = sum([p for p , _ in items]) 
        mitad = total/2
        acum = 0
        i = 0
        while (acum < mitad):
            acum += items[i][0]
            i += 1
        i -= 1
        
        # decidir punto de corte
        diferenciaAnt = abs((acum - items[i][0]) - mitad)
        diferenciaAct = abs(acum - mitad)
        if (diferenciaAct > diferenciaAnt):
            acum -= items[i][0]
            i -= 1
        
        # colocar bits, llamado recursivo
        i += 1

        mitad1 = items[0:i]
        mitad2 = items[i:]

        for x in mitad1:
            x[1] += "0"
        for y in mitad2:
            y[1] += "1"

        shannonFanoRecursivo(mitad1)
        shannonFanoRecursivo(mitad2)


def binarioACadena(binario,cantBitsRelleno):
    cadena = ""

    for byte in binario:
        cadena += format(byte,"08b")
        
    if (cantBitsRelleno > 0):
        cadena = cadena[:-cantBitsRelleno]
        
    return cadena
        

def cadenaABinario(cadenaBinaria): # me pasan, por ej, '01001010' si el largo de la cadena no es multiplo de 8, relleno con 0?? -- len(cadena) != 8 * i
    binario = bytearray()
    # cuantos bits de relleno vamos a agregar
    # si tenemos '01011' el resto es 5 y entonces hay 3 bits de relleno
    # si tenemos '01011001' el resto da 8, y el segundo %8 da 0 bits de relleno
    cantBitsRelleno = (8 - len(cadenaBinaria) % 8) % 8
    cadenaBinaria += "0" * cantBitsRelleno # uso 0 arbitrariamente
    
    for i in range(0,len(cadenaBinaria),8): # me muevo de a 8 bits
        byte = cadenaBinaria[i:i+8]
        binario.append(int(byte,2)) # transformo la porción de 8 bits de la cadena binaria a enteros, siendo la cadena en base 2

    return binario, cantBitsRelleno



# -- SIN BYTEARRAY --

def codificar(alfabeto,palabrasCodigo,mensaje):
    msjCodificado = ""
    palabraFuente = ""

    for c in mensaje: # c de caracter
        palabraFuente += c
        if (palabraFuente in alfabeto):
            i = alfabeto.index(palabraFuente)
            msjCodificado += palabrasCodigo[i]
            palabraFuente = ""        

    return msjCodificado

def decodificar(alfabeto,codigo,mensaje):
    msjDecodificado = ""
    palabraCodigo = ""

    for b in mensaje: # b de bit
        palabraCodigo += b
        if (palabraCodigo in codigo):
            i = codigo.index(palabraCodigo)
            msjDecodificado += alfabeto[i]
            palabraCodigo = ""

    return msjDecodificado



# -- CON BYTEARRAY --

def codificarByteArray(alfabeto,palabrasCodigo,mensaje): # mensaje fuente ("ABwOz") ; devuelve byteArray y cantBitsRelleno
    # explicación bits relleno
    # si tenemos '010' y lo pasamos a bytearray, o rellenamos con 0 al principio o al final
    # y luego para decodificar debemos saber que esos 0 son relleno y no información real del mensaje original
    # 010 + 00000 -> 010
    msjCodificado = ""
    palabraFuente = ""

    for c in mensaje:
        palabraFuente += c
        if (palabraFuente in alfabeto):
            i = alfabeto.index(palabraFuente)
            msjCodificado += palabrasCodigo[i]
            palabraFuente = ""        

    return cadenaABinario(msjCodificado)

def decodificarByteArray(alfabeto,codigo,binario,cantBitsRelleno): # mensaje codificado en bytearray y las cantidades de bits de relleno para distinguir de la información original
    msjDecodificado = ""
    palabraCodigo = ""

    mensaje = binarioACadena(binario,cantBitsRelleno)

    for b in mensaje: # b de bit
        palabraCodigo += b
        if (palabraCodigo in codigo):
            i = codigo.index(palabraCodigo)
            msjDecodificado += alfabeto[i]
            palabraCodigo = ""

    return msjDecodificado

def obtenerTasaCompresion(cadenaOriginal,cadenaComprimida):
    largoOg = len(cadenaOriginal)
    largoComp = len(cadenaComprimida)
    proporcion = largoOg / largoComp
    return proporcion

def comprimirRLC(mensaje): # recibe mensaje tipo string, devuelve string formato "L2T3M1", la función es case sensitive
    res = bytearray()
    cant = 1
    letra = mensaje[0]
    if (len(mensaje) > 1):
        for c in mensaje[1:]:
            if (c != letra):
                res.append(ord(letra))
                res.append(cant)
                cant = 1
                letra = c
            else:
                cant += 1
    res.append(ord(letra))
    res.append(cant)
    return res
















# ------------------- CANALES Y CODIFICACIÓN ------------------- 

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

# ---------------------     P(B)     ---------------------
def generarProbabilidadesSalida(probabilidadesPriori,matrizCanal): # P(B)
    probSalida = []
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    for j in range(s):
        probSalida.append(0)
        for i in range(r):
            probSalida[j] += probabilidadesPriori[i] * matrizCanal[i][j]
            
    return probSalida

# ---------------------     P(ai/bj)     ---------------------
def generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matrizCanal): # P(ai/bj)
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    matrizPosteriori = [[0] * s for _ in range(r)]
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    
    for i in range(r):
        for j in range(s):
            if (probsSalida[j] > 0):
                matrizPosteriori[i][j] = (matrizCanal[i][j] * probabilidadesPriori[i]) / probsSalida[j]
            else:
                matrizPosteriori[i][j] = 0
            
    return matrizPosteriori

# ---------------------     P(ai,bj)     ---------------------
def generarMatrizProbabilidadesEventosSimultaneos(probabilidadesPriori,matrizCanal): # P(ai,bj)
    r = len(probabilidadesPriori)
    s = len(matrizCanal[0])
    matrizEventosSimultaneos = [[0] * s for _ in range(r)]
    
    for i in range(r):
        for j in range(s):
            matrizEventosSimultaneos[i][j] = matrizCanal[i][j] * probabilidadesPriori[i]
            
    return matrizEventosSimultaneos

# ---------------------     H(A,b)     ---------------------
def generarEntropiasPosteriori(probabilidadesPriori,matriz): # H(A/b)
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

# ---------------------     H(A/B)     ---------------------
def obtenerRuido(probabilidadesPriori,matrizCanal): # H(A/B)
    s = len(matrizCanal[0])
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    entropiasPost = generarEntropiasPosteriori(probabilidadesPriori,matrizCanal) 

    ruido = 0
    for j in range(s):
        ruido += probsSalida[j] * entropiasPost[j]
    return ruido

# ---------------------     H(B/A)     ---------------------
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


# ---------------------     H(A,B)     ---------------------
def obtenerEntropiaAfin(probabilidadesPriori,matrizCanal): # H(A,B) # entropia afín <-> entropía conjunta
    entropiaPriori = obtenerEntropia(probabilidadesPriori,2)
    entropiaSalida = obtenerEntropia(generarProbabilidadesSalida(probabilidadesPriori,matrizCanal),2)
    informacionMutua = obtenerInformacionMutua(probabilidadesPriori,matrizCanal)
    return entropiaPriori + entropiaSalida - informacionMutua


# ---------------------     I(A,B)     ---------------------
def obtenerInformacionMutua(probabilidadesPriori,matrizCanal): # I(A,B)
    entropiaPriori = obtenerEntropia(probabilidadesPriori,2)
    ruido = obtenerRuido(probabilidadesPriori,matrizCanal)
    return entropiaPriori - ruido



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


def columnasSonCombLineal(matrizCanal,j1,j2,usarIsclose=False):
    aux = True
    r = len(matrizCanal)
    i = 0
    while (i<r and matrizCanal[i][j1] == 0):
        i += 1
    if (i == r):
        aux = False
    else:
        proporcion = matrizCanal[i][j2] / matrizCanal[i][j1] # factor que multiplica a la primera columna para ser igual a la segunda (el orden es arbitrario)
    i = 0
    while (aux and i<r):
        if (usarIsclose):
            aux = math.isclose(matrizCanal[i][j1] * proporcion,matrizCanal[i][j2])
        else:
            aux = matrizCanal[i][j1] * proporcion == matrizCanal[i][j2]     
        i += 1
    return aux
    
def generarMatrizDeterminante(matrizCanal,j1,j2):
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    matrizDeterminante = [[0] * (s-1) for _ in range(s)]
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


def esReducible(matriz): # devuelve las columnas j1 y j2 (que son CL), en caso de no ser reducible devuelve (-1,-1)
    # comprobación de reducción posible
        aux = False
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
        # imprimirMatriz(matriz)
        matDet = generarMatrizDeterminante(matriz,j1,j2)
        matriz = generarMatrizCompuesta(matriz,matDet)
        # imprimirMatriz(matDet)
        # imprimirMatriz(matriz)
    return matriz


def capacidadCanalDeterminante(matrizCanal): # invocar sólo si se verificó que el canal sea DETERMINANTE
    return math.log2( len(matrizCanal[0]) ) # log2(s) , s= cantSalidas

def capacidadCanalSinRuido(matrizCanal): # invocar sólo si se verificó que el canal sea SIN RUIDO
    return math.log2( len(matrizCanal) ) # log2(r) , r= cantidadEntradas


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

    capacidad = infoMaxima
    return capacidad, pMaximo


def obtenerProbabilidadError(probabilidadesPriori,matrizCanal,tomarEstrellaPosteriori=True): # el booleano opcional decide el criterio para elegir a*
    r = len(matrizCanal)
    s = len(matrizCanal[0])
    matProbsPost = generarMatrizProbabilidadesPosteriori(probabilidadesPriori,matrizCanal)
    probsSalida = generarProbabilidadesSalida(probabilidadesPriori,matrizCanal)
    probsError = [0] * s

    # Franco me dijo que a* se obtiene de la matriz del canal
    # pero en las filminas se obtiene a partir de la matriz a posteriori
    # y también a mí me hace más sentido

    if(tomarEstrellaPosteriori): # si tomo criterio de elección según matriz a posteriori
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

    else: # si tomo criterio de elección según matriz del canal       
        for j in range(s):
            aEstrella = -1
            valMaximo = 0
            for i in range(r):
                if (matrizCanal[i][j] > valMaximo):
                    valMaximo = matrizCanal[i][j]
                    aEstrella = i
            valMaximo = matProbsPost[aEstrella][j]
            probsError[j] = 1 - valMaximo

    probabilidadError = 0
    for j in range(s):
        probabilidadError += probsError[j] * probsSalida[j]

    return probabilidadError



'''
1) Dado el siguiente mensaje binario:

a) Estimar la entropía de la fuente de información que lo generó
b) Generar un código binario óptimo para la fuente de información
c) Generar códigos binarios óptimos para las extensiones de orden 2 y 3
d) Calcular la longitud media, el rendimiento y la redundancia de cada código
'''
consigna1 = "1) Dado el siguiente mensaje binario:\na) Estimar la entropía de la fuente de información que lo generó\nb) Generar un código binario óptimo para la fuente de información\nc) Generar códigos binarios óptimos para las extensiones de orden 2 y 3\nd) Calcular la longitud media, el rendimiento y la redundancia de cada código\n"

def main():
    print("2do Parcial 2026:")
    print("--- Ejercicio 1 ---\n\n")

    print(consigna1,"\n\n")
    msj = "000001000100000100110000001000"
    print("Msj binario: ",msj)

    #a)
    print("a)")
    # msjBytearray, bitsRelleno = cadenaABinario(msjCadena)
    # decodificarByteArray(,msjBytearray,bitsRelleno)
    probs = generarProbabilidades(msj)
    entropia = obtenerEntropia(probs,2)
    print("Probabilidades P = ",probs)
    print("Entropía Hr(S) = ",entropia,"\n")


    #b)
    print("b)")
    codigo = generarCodigoHuffman(probs)
    print("Código óptimo, por huffman: ",codigo,"\n")
    
    #c)
    print("c)")
    probsExtDos = generarExtensionProbabilidades(probs,2)
    probsExtTres = generarExtensionProbabilidades(probs,3)
    codigoDos = generarCodigoHuffman(probsExtDos)
    codigoTres = generarCodigoHuffman(probsExtTres)

    print("Código óptimo, por Huffman, para la extensión de orden 2")
    print(codigoDos,"\n")

    print("Código óptimo, por Huffman, para la extensión de orden 3")
    print(codigoTres,"\n\n")


    #d)
    print("d)")
    longMediaOg = obtenerLongitudMedia(codigo,probs)
    longMediaDos = obtenerLongitudMedia(codigoDos,probsExtDos)
    longMediaTres = obtenerLongitudMedia(codigoTres,probsExtTres)    

    rendimientoOg, redundanciaOg = obtenerRendimientoCodigo(codigo,probs)
    rendimientoDos, redundanciaDos = obtenerRendimientoCodigo(codigoDos,probsExtDos)
    rendimientoTres, redundanciaTres = obtenerRendimientoCodigo(codigoTres,probsExtTres)

    print(f"Longitud Media, código original, L = {longMediaOg}")
    print(f"Longitud Media, extensión orden 2, L2 = {longMediaDos:.4f}")
    print(f"Longitud Media, extensión orden 2, L2/2 = {(longMediaDos/2):.4f}")
    print(f"Longitud Media, extensión orden 2, L3 = {longMediaTres:.4f}")
    print(f"Longitud Media, extensión orden 3, L3/3 = {(longMediaTres/3):.4f}\n")

    print(f"Código original \n- Rendimiento: {rendimientoOg:.4f} \n- Redundancia: {redundanciaOg:.4f} \n")
    print(f"Código ext ord 2 \n- Rendimiento: {rendimientoDos:.4f} \n- Redundancia: {redundanciaDos:.4f} \n")
    print(f"Código ext ord 3 \n- Rendimiento: {rendimientoTres:.4f} \n- Redundancia: {redundanciaTres:.4f} \n")

main()