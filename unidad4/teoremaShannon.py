import math
'''
1. Codificar una función booleana en Python que reciba como parámetros: una lista con la
distribución de probabilidades de una fuente, otra lista con palabras código para la
extensión de orden N y el valor de N, y verifique si el código cumple con el Primer Teorema
de Shannon. '''

def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

def obtenerEntropia(probabilidades, informaciones):
    suma = 0
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

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
def cumpleShannon(palabrasCodigo, probabilidades, n):
# Está mal esto, tengo que pasar el código para la extensión
# y calcular el código acorde antes de llamar a la función
# el dolor de huevos está en calcular un código eficiente (que es complejo por su largo)
#
'''
    palabrasCodigoExt, probabilidadesExt = generarExtensionFuente(palabrasCodigo,probabilidades,n)
    entropia = obtenerEntropia(probabilidades,generarListaInformacion(probabilidades,len(generarAlfabetoCodigo(palabrasCodigo))))
    longMedia = obtenerLongitudMedia(palabrasCodigoExt, probabilidadesExt)
    longMedia /= n # longMedia == Ln / n
    return (longMedia >= entropia ) and (longMedia < (entropia + 1/n) )
'''
    
def ej1(palabrasCodigo,probabilidades,n):
'''    codExt, probExt = generarExtensionFuente(palabrasCodigo,probabilidades,n)
    print("Código: ",palabrasCodigo)
    print("Probabilidades: ",probabilidades)
    print()
#    print("Código Extendido: ",codExt)
#    print("Probabilidades Extendidas: ",probExt)
    print()
    print("Hr(S) = ",obtenerEntropia(probabilidades,generarListaInformacion(probabilidades,len(generarAlfabetoCodigo(palabrasCodigo)))))
    print("Ln / n = ",obtenerLongitudMedia(codExt,probExt)/n)
    print("Hr(S) + 1/n = ",obtenerEntropia(probabilidades,generarListaInformacion(probabilidades,len(generarAlfabetoCodigo(palabrasCodigo)))) + 1/n)
    print()
    print("Cumple Shannon?")
    print(cumpleShannon(palabrasCodigo,probabilidades,n))
'''
    
def main():
    cod1 = ['00','01','10','11']
    prob1 = [0.25,0.25,0.25,0.25]

    prob2 = [0.025,0.025,0.9,0.05]
    ej1(cod1,prob2,10)


main()