#halloooooo Leute
import math

def obtenerEntropia(probabilidades, r):
    suma = 0
    informaciones = generarListaInformacion(probabilidades,r)
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

def generarListaInformacion(probabilidades,r):
    return [math.log(1/prob,r) if prob > 0 else 0 for prob in probabilidades]

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

def obtenerLongitudMedia(palabrasCodigo, probabilidades):
    return sum([prob * len(palabra) for palabra,prob in zip(palabrasCodigo, probabilidades)])

def obtenerRendimientoCodigo(codigo,probabilidades): # retorna rendimiento, redundancia (η, R)
    alfabetoCodigo = generarAlfabetoCodigo(codigo)
    r = len(alfabetoCodigo)
    entropia = obtenerEntropia(probabilidades, r)
    longMedia = obtenerLongitudMedia(codigo,probabilidades)
    return entropia / longMedia , 1 - (entropia / longMedia)

def generarAlfabetoCodigo(palabrasCodigo):
    alfabetoCodigo = []
    for palabra in palabrasCodigo:
        for caracter in palabra:
            if caracter not in alfabetoCodigo:
                alfabetoCodigo.append(caracter)
    return alfabetoCodigo




''' 3. Desarrollar dos funciones en Python que reciban como parámetro una lista con la
    distribución de probabilidades de una fuente de información y generen una lista de
    cadenas de caracteres con codificaciones binarias de Huffman y de Shannon-Fano. '''
    
''' Implementación en Python (gracias Franco)

    como cada elemento es una lista, lo que se tiene en la lista original son referencias a cada elemento,
    si luego se hace una copia ordenada, el orden de la nueva lista es distinto, y se pueden modificar los elementos,
    modificandolos en la lista original pero sin alterar el orden original en la variable original

    def algoritmo(probs):
    items = [[p, ""] for p in probs] 
    codificar(sorted(items))
    return [code for _, code in items] '''
    
    
# dios wacho, hace una banda que no hago funciones recursivas


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


def pruebaHuffmanYShannon():
    probabilidades = [0.26,0.40,0.24,0.10]
    print("Probabilidades = ",probabilidades,"\n")

    shannonFano = generarCodigoShannonFano(probabilidades)
    print("Shannon Fano: ",shannonFano,"\n")
    # bien, Shannon anda
    
    huffman = generarCodigoHuffman(probabilidades)
    print("Huffman: ",huffman)
    # .....
    
    print("\n")

''' 4. Para una fuente de información con distribución de probabilidades:
    P = { 0.385, 0.154, 0.128, 0.154, 0.179 }
    a. Calcular la entropía de la fuente
    b. Generar una codificación de Huffman
    c. Obtener una codificación de Shannon-Fano
    d. Graficar los árboles binarios que surgen de cada codificación
    e. Comparar la longitud media, el rendimiento y la redundancia de cada código '''
    
def ej4():
    probs = [0.385,0.154,0.128,0.154,0.179]
    print("Entropia: ",obtenerEntropia(probs,2)," bits")
    print(generarCodigoHuffman(probs))
    print(generarCodigoShannonFano(probs))
    
''' 5. Dada una fuente de información que emite el siguiente mensaje representativo:
    58784784525368669895745123656253698989656452121702300223659
    a. Calcular la entropía de la fuente
    b. Construir una codificación de Huffman
    c. Generar una codificación de Shannon-Fano
    d. Comparar la longitud media, el rendimiento y la redundancia de cada código '''
    
def ej5():
    alfabeto, probs = generarFuente("58784784525368669895745123656253698989656452121702300223659")
    print("Alfabeto: ",alfabeto)
    print("Probabilidades : ",[f"{p:.4f}" for p in probs])
    print(f"Entropia: {obtenerEntropia(probs,2):.4f} bits")

    huffman = generarCodigoHuffman(probs)
    shannonFano = generarCodigoShannonFano(probs)

    print("\nHuffman = ",huffman)
    print(f"Long Media = {obtenerLongitudMedia(huffman,probs):.4f}")
    rend, redun = obtenerRendimientoCodigo(huffman,probs)    
    print(f"Rendimiento = {rend:.4f}")
    print(f"Redundancia = {redun:.4f}")
    
    print("\n\nShannon-Fano: ",shannonFano)
    print(f"Long Media = {obtenerLongitudMedia(shannonFano,probs):.4f}")
    rend, redun = obtenerRendimientoCodigo(shannonFano,probs)    
    print(f"Rendimiento = {rend:.4f}")
    print(f"Redundancia = {redun:.4f}")
    

''' 11. Realizar una función en Python que reciba como parámetro una cadena de caracteres con
    un mensaje y devuelva una secuencia de bytes (bytearray) que contenga el mensaje
    comprimido con RLC, utilizando un byte para almacenar la representación en código ASCII
    del carácter y otro byte para el número. '''

def comprimirRLC(mensaje): # recibe mensaje tipo string, devuelve string formato "L2T3M1", la función es case sensitive
    res = ""
    cant = 1
    letra = mensaje[0]
    if (len(mensaje) > 1):
        for c in mensaje[1:]:
            if (c != letra):
                res += letra
                res += str(cant)
                cant = 1
                letra = c
            else:
                cant += 1
    res += letra
    res += str(cant)
    return res
    
    
''' 12. Volver a comprimir los mensajes del ejercicio 10 (utilizando la función desarrollada) y
    calcular la tasa de compresión de cada uno. '''

def obtenerTasaCompresion(original,comprimido):
    largoOg = len(original)
    largoComp = len(comprimido)
    proporcion = round(largoOg / largoComp)
    return str(proporcion) + ":1"
    
def ej12():
    msjA = "XXXYZZZZ"
    msjB = "AAAABBBCCDAA"
    msjC = "UUOOOOAAAIEUUUU"
        
    lista = [msjA,msjB,msjC,"0000000000000kkkkqqqqqqWWWWWWWWWWWWWWWWW"]
    
    for x in lista:
        print("Mensaje: ",x)
        print("Mensaje Comprimido mediante RLC: ",comprimirRLC(x) )
        print("Tasa de Compresión: ",obtenerTasaCompresion(x,comprimirRLC(x)) )
        print("\n")


        
       
def main():
    print("rn: Listening to Supertramp\n")
#    pruebaHuffmanYShannon()
#    ej4()
#    ej5()
    ej12()
    
print()
main()
print()