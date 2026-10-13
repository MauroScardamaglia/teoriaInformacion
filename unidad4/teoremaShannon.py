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

def verificarParidad(msj):
    return msj[0:len(msj)-1].count('1') == int(msj[len(msj)-1])


def darRedundanciaMensaje(c,mostrar = False):
    cad = ord(c)
    if (mostrar): print(cad)

    cad = bin(cad)
    cad = cad[2:]
    if (mostrar): print(cad)
    # bin devuelve un string "0b0010101010"

    cad += str(cad.count('1') % 2)
    if (mostrar): print(cad)
    return cad

def ej12():
    mensajeConRedundancia = darRedundanciaMensaje('C',True)
    print(mensajeConRedundancia)
    print(verificarParidad(mensajeConRedundancia))


def main():
#    prueba()
#    ej2()
#    ej3()
#    ej4()
#    ej5()
#    ej7()
#    ej9()
#    ej10()
    ej12()

print()
main()
print()

# α = 5