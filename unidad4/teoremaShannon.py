import math
'''
1. Codificar una función booleana en Python que reciba como parámetros: una lista con la
distribución de probabilidades de una fuente, otra lista con palabras código para la
extensión de orden N y el valor de N, y verifique si el código cumple con el Primer Teorema
de Shannon. '''

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
def cumpleShannon(palabrasCodigo, probabilidades, n,mostrar = False):
# Las probabilidades que recibo son las de la fuente original, q probabilidades
#
# Tengo que pasar el código para la extensión
# y calcular el código acorde antes de llamar a la función
# el dolor de huevos está en calcular un código eficiente (que es complejo por su largo)
#
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
#    q = len(probabilidades)
#    aux, probabilidadesExt = generarExtensionFuente(["a"]*q,probabilidades,n)
    probabilidadesExt = generarExtensionProbabilidades(probabilidades,n)
    entropia = obtenerEntropia(probabilidades, len(alfabetoCodigo))

    longMedia = obtenerLongitudMedia(palabrasCodigo,probabilidadesExt)
    cotaInf = entropia
    cotaSup = entropia + 1/n

    print("Hr(S) = ",cotaInf)
    print("Ln/n = ",longMedia/n)
    print("Hr(S) + 1/n = ",cotaSup)

    return (cotaInf <= longMedia/n) and (longMedia/n < cotaSup)    

    
def ej1(palabrasCodigo,probabilidades,n):
    alfabetoCodigo = generarAlfabetoCodigo(palabrasCodigo)
#    q = len(probabilidades)
#    aux, probabilidadesExt = generarExtensionFuente(["a"]*q,probabilidades,n)
    probabilidadesExt = generarExtensionProbabilidades(probabilidades,n)
    print("Alfabeto Código: ",alfabetoCodigo)
    print("Probabilidades: ",probabilidades)
    print("Probabilidades para la extensión de orden ",n,": ",probabilidadesExt)
    print("Código para la extensión de orden ",n,": ",palabrasCodigo)
    print("\nCumple Shannon?\n")
    if (cumpleShannon(palabrasCodigo,probabilidades,n,True)):
        print("\nSí")
    else:
        print("\nNo")


def prueba():
    prob = [0.5,0.45,0.05]
    codigo = ["00","10","01100","11","010","01110","01101","011110","011111"]
    
    ej1(codigo,prob,2)    


def ej2():
        prob = [0.3,0.1,0.4,0.2]
        cod = ["BA","CAB","A","CBA"]
        ej1(cod,prob,1)

        print()
        print()
        print()
        
        codExt, probExt = generarExtensionFuente(cod,prob,2)
        ej1(codExt,prob,2)
    
def ej3():
    prob = [0.5,0.2,0.3]
    c1 = ["11","010","00"]
    c2 = ["10","001","110","010","0000","0001","111","0110","0111"]

    ej1(c1,prob,1)
    print("\n\n")
    ej1(c2,prob,2)

def ej4():
    c3 = ["0","100","101","11100","110","11101","11110","11111"]
    probs = [0.8,0.2]

    ej1(c3,probs,3)
    
def ej5():
    probs = [0.7,0.3]
    huff1 = ["0","1"]
    shannonFano2 = ["0","10","110","111"]
    ej1(huff1,probs,1)
    print("\n\n")
    ej1(shannonFano2,probs,2)
    

''' 6. Realizar una función en Python que reciba como parámetros: dos listas paralelas con la
    distribución de probabilidades de una fuente y su codificación, y calcule el rendimiento y la
    redundancia del código. '''

def obtenerRendimientoCodigo(codigo,probabilidades): # retorna rendimiento, redundancia (η, R)
    alfabetoCodigo = generarAlfabetoCodigo(codigo)
    r = len(alfabetoCodigo)
    entropia = obtenerEntropia(probabilidades, r)
    longMedia = obtenerLongitudMedia(codigo,probabilidades)
    return entropia / longMedia , 1 - (entropia / longMedia)

def ej7():
    c1 = ["11","010","00"]
    probs = [0.5,0.2,0.3]
    
    c2 = ["10","001","110","010","0000","0001","111","0110","0111"]
    probsExtOrd2 = generarExtensionProbabilidades(probs,2)

    η1, R1 = obtenerRendimientoCodigo(c1,probs)
    η2, R2 = obtenerRendimientoCodigo(c2,probsExtOrd2)
    
    print("Rendimiento η1 = ",η1)
    print("Redundancia R1 = ",R1)
    print("Rendimiento η2 = ",η2)
    print("Redundancia R2 = ",R2)

''' 10. Implementar una función en Python que reciba una lista de cadenas de caracteres que
    representa una codificación binaria y devuelva: la distancia de Hamming, la cantidad de
    errores que se pueden detectar y la cantidad de errores que se pueden corregir '''

def obtenerDistanciaHamming(cad1,cad2):
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


def verificarHamming(codigo): # retorna dMin (distancia de Hamming del código), alpha y beta (cant errores máxima detectables y corregibles, respectivamente)               
    print("Código: ",codigo)
    dMin,alpha,beta = obtenerDistanciaHammingCodigo(codigo)
    print("DMin: ",dMin)
    print("Máxima cantidad de errores detectables (α):",alpha)
    print("Máxima cantidad de errores corregibles (β):",beta)
    print()

def ej9():
    verificarHamming(["00","01","10","11"])
    verificarHamming(["000","100","101","111"])
    verificarHamming(["0000","0011","1010","0101"])

def ej10():
    verificarHamming(["0100100","0101000","0010010","0100000"])
    verificarHamming(["0100100","0010010","0101000","0100001"])
    verificarHamming(["0110000","0000011","0101101","0100110"])

''' 12. Desarrollar funciones en Python que resuelvan lo siguiente:
    a. Dado un carácter, devolver un byte que represente su código ASCII (7 bits) y utilice
    el bit menos significativo para almacenar la paridad del código.
    b. Dado un byte que se obtuvo como resultado de la función anterior, verificar si es
    correcto o tiene errores. '''

#def verificarParidad(msj,mostrar = False): # claro, paridad par (cantidad par de 1's -> 0)
#    if (mostrar): print(msj[0:-1].count('1') % 2)
#    if (mostrar): print(int(msj[len(msj)-1]))
#    return (msj[0:-1].count('1') % 2) == int(msj[-1])

# más fácil:
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

def ej12():
    mensajeConRedundancia = darRedundanciaCaracter('C',True)
    print(verificarParidad(mensajeConRedundancia),end="\n\n")

    mensajeConRedundancia = darRedundanciaCaracter('0',True)
    print(verificarParidad(mensajeConRedundancia),end="\n\n")

    mensajeConRedundancia = darRedundanciaCaracter('a',True)
    print(verificarParidad(mensajeConRedundancia),end="\n\n")

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


''' 13. Dadas las siguientes matrices que contienen mensajes representados con código ASCII y
    sus bits de paridad vertical, longitudinal y cruzada, detectar los errores y, en caso de ser
    posible, recuperar el mensaje original: '''

def ej13():
    a = [list("00100001"),list("10000111"),list("10000010"),list("10100110"),list("10000010")]
    b = [list("00101101"),list("10011001"),list("10001010"),list("10011100"),list("10000010")]
    c = [list("00101010"),list("10000010"),list("10011010"),list("10011111"),list("10100101")]
    d = [list("00010100"),list("10010000"),list("10011110"),list("10011001"),list("10000010")]
    e = [list("00110101"),list("10011010"),list("10101011"),list("10100100"),list("10000010")]
    f = [list("00001001"),list("10101001"),list("10100101"),list("10001011"),list("10100110")]
    g = [list("00011101"),list("10010011"),list("10011101"),list("10001100"),list("10011111")]
    h = [list("00111110"),list("10000111"),list("10010000"),list("10000010"),list("10101010")]
    lista = [a,b,c,d,e,f,g,h]
    for c,msj in zip(["a","b","c","d","e","f","g","h"],lista):
        print(c)
        print("----  ----  ----  ----  ----")
        print("Msj Recibido:")
        imprimirMensajRedund(msj)
        print("\nMensaje original:")
        imprimirMensajRedund(corregirMensaje(msj))
        print("\n\n\n\n")


''' 14. Codificar funciones en Python que resuelvan lo siguiente:
    a.  Dada una cadena de caracteres, generar una secuencia de bytes (bytearray) que
    contenga su representación con código ASCII y sus bits de paridad vertical,
    longitudinal y cruzada.
    
    b.  Dada una secuencia de bytes que se obtuvo como resultado de la función anterior,
    devolver el mensaje original o una cadena de caracteres vacía si no se pueden
    corregir los errores.

    Sugerencia: generar una matriz de bits para realizar las operaciones, transformando la
    secuencia de bytes en una lista de cadenas de caracteres binarias y, luego, cada cadena
    de caracteres en una lista de números enteros que representen los bits.
    
    Lo hago a mi manera xD
'''

# a)
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
    
# b)
def corregirMensaje(mensaje): # devuelve el mensaje original, si no había errores o se pueden corregir; caso contrario devuelve algo gracioso xD
    # almacenan i y j's
    filasConErrores = [] 
    colConErrores = [] 
    
    n = len(mensaje)
    m = len(mensaje[0])

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
        if (mensaje[i][j] == "0"):
            mensaje[i][j] = "1"
        else:
            mensaje[i][j] = "0"
        return mensaje        
            
def pruebaCrearMensajes():
    generarMensajeConParidades("Hallo",True)
    print("\n\n")
    generarMensajeConParidades("Luke",True)
    print("\n\n")
    generarMensajeConParidades("meinNeu160mlMate",True)
            
def main():
    aux = 0 # por poner algo xD
#    prueba()
#    ej2()
#    ej3()
#    ej4()
#    ej5()
#    ej7()
#    ej9()
#    ej10()
#    ej12()
#    mat = [[0]*5]*5
#    print(mat)
#    imprimirMensajRedund([[0]*5]*5)
#    ej13()
#    pruebaCrearMensajes()

#           ---------------------------------------------            DOY POR TERMINADA LA GUÍA           ---------------------------------------------
    

print()
main()
print()

# α = 5