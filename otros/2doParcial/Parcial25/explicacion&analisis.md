\--Ejercicio 1--



* Explicación del código:



a) Para obtener las probabilidades de los símbolos fuentes uso una función sencilla que cuenta apariciones de cada letra. Luego para la entropía de la fuente, se suma por cada símbolo su probabilidad por el logaritmo, en este caso de base 2, del inverso de la probabilidad, trivial.



b) Luego para generar el código binario óptimo utilizo Huffman, ya que Shannon-Fano no garantiza un código óptimo que alcance la cota L < Hr(S) + 1, Huffman sí; Además me gusta más Huffman. Huffman es un proceso recursivo en el que en cada iteración se juntan los símbolos o grupos de símbolos con menos probabilidades, así dandole prioridad (menor longitud) a los símbolos con mayores probabilidades.



c) La función que calcula tasas de compresión es también sencilla, divide el largo original por el comprimido.





d) Para la extensión de orden 3 utilizo también Huffman, pero con las probabilidades extendidas, es decir las de la fuente de extensión de orden 3.

Para obtener estas probabilidades extendidas, recorro las q^n combinaciones de probabilidades, agregando en cada combinación la probabilidad extendida a las probabilidades a devolver, esta probabilidad es la multiplicación entre las probabilidades de la combinación. Ejemplo, si en mi iteración actual quiero agregar la probabilidad de GIF, tengo que multiplicar 0.3\*0,3\*0.05 -> 0.0045



e) Para calcular Longitud Media, en cada caso voy sumando, por cada símbolo de la fuente su probabilidad por su longitud sum(i) (p(i)\*li). Para calcular rendimiento se divide la entropía de la fuente por la Longitud media, esto da un rango entre (0,1], yo a veces me confundo cual es denominador y cual numerador, pero me acuerdo que como la longitud media tiene de piso a la entropía entonces la longitud siempre va a estar en el denominador ya que esta razón tiene como techo a 1 ya que es un valor entre 0 y 1. La redundancia es simplemente el complemento del rendimiento. Para mostrar la longitud media de la extensión de orden 3, la divido por 3 (Ln/3) para ser coherente con el análisis sobre la fuente original, esto no es necesario para el rendimiento ya que evaluar sobre la fuente original o sobre la extendida es equivalente matemáticamente << Hr(s^n) / Ln <-> Hr(S) / (Ln/n) >>.



f) Para verificar si un código cumple con el Primer Teorema de Shannon es necesario verificar que su longitud media es mayor o igual a la entropía de su fuente y menor a esa misma cota + 1.





* Análisis:



a) Las probabilidades no son tan equitativas, pero si se acercan levemente, esto hace sentido a que su entropía sea de 1.78bits, 0.22 bits de diferencia con su máxima entropía posible dado 4 símbolos, 2.00.



b) Lo anterior se refleja en el código obtenido a través del algoritmo de Huffman que devuelve 4 palabras código con misma longitud.



c)  Codificando el mensaje se obtiene una tasa de compresión de 4.0:1, lo cual además de ser un número muy impoluto, es interesante, porque dada la equidad entre las longitudes de los 4 símbolos, que tienen 2 binits de largo, teniendo en cuenta que el largo original de los símbolos era un byte, por ser ascii, se pasa en todos los símbolos de 8 a 2 binits, una compresión bastante decente.



d) Este código, siguiendo el primer teorema de shannon, debería acercar más su longitud media (Ln/n) a la entropía, ya que tiene un n (3) mayor al original (1). Recordar que con un n suficientemente grande, Ln/n -> Hr(S).



e) Lo anterior se refleja en el análisis actual. La longitud media L del primer código es 2.00, la Ln/n del código hecho a partir de la extensión de orden 3 es 1.7945, muy cerca de la entropía que es 1.7884, es decir que tan solo con una extensión de orden 3 ya nos acercamos bastante a la cota inferior del teorema de shannon, aunque claro, el código ahora pasa de tener 4 palabras código a 4^3, 64 palabras código. El rendimiento y la redundancia con dependientes de la longitud media, así que no tengo mucho para decir, salvo que el rendimiento pasa de 89.42% a 99.66%, reafirmando lo anteriormente dicho.



f) Ámbos códigos cumplen el teorema de shannon, lógico, ámbos usan Huffman por lo que respetan la cota superior, y por un límite físico cumplen la cota inferior.







\-- Ejercicio 2 --



* Explicación de código



a) Las probabilidas a priori P(A) se obtienen de la misma manera que el inciso a anterior, la matriz del canal se obtiene sumando apariciones en las celdas M\[i]\[j], del par ai, bj, luego normalizando diviendo cada elemento de la matriz por la sumatoria de su fila, haciendo que las filas sumen 1, ya que la matriz analiza probabilidades de salida dada la entrada.



b) Para verificar la propiedad de ser determinante o sin ruido se analiza la característica de haber una sola probabilidad no nula en cada fila y cada columna, respectivamente.



c) Para calcular el ruido H(A/B) se suman las multiplicaciones entre P(b)\*H(A/b), esta última se obtiene de la matriz de probabilidades a posteriori, obtenida a su vez a través del teorema de bayes. Para calcular la pérdida H(B/A) se suman las multiplicaciones entre P(a)\*H(B/a), esta última se obtiene a partir de la matriz del canal, es decir la ya obtenida. Para calcular la información mutua se resta la entropía de la salida menos la pérdida, ó la entropía de la entrada menos el ruido. Yo implemenenté de la primera forma (o la otra, no me acuerdo xd).



d) Para reducir la matriz del canal, se ejecuta un bucle while donde mientras haya reducciones posibles se reduce el canal, generando la matriz determinante para 2 columnas reducibles, se hace el producto matricial, es decir se genera la matriz compuesta de la matriz actual por la determinante. Luego con la matriz compuesta se repite el bucle. 

Para verificar si se puede reducir, se buscan columnas que sean combinación lineal entre sí, es decir que todos los elementos de la segunda columna sean el análogo en la primera columna multiplicada por una proporción.

Para generar la matriz determinante, dadas las 2 columnas j1,j2 se genera una matriz s\*(s-1) donde cada fila representa la columna original, y tiene un 1 solo en distintas columnas, excepto por la fila que representa la segunda columna que es igual a la fila que representa la primera columna.
Para generar la matriz compuesta simplemente se hace un producto matricial.

e) Para determinar una capacidad de una manera sencilla hay 3 vías, si la matriz es determinante, sin ruido o binaria, en este caso, como la matriz reducida es 2x2, utilizo la 3ra opción. Para calcular la capacidad de una matriz binaria, se pasa como parámetro la matriz binaria y un valor de paso, se inicializa p en 0, y se va avanzando con p+=paso hasta que p > 1. Esto asegura probar muchas combinaciones de P(A) = \[p,1-p], hasta encontrar, con cierta sensibilidad otorgada por la precisión del valor de paso, las probabilidades a priori que garantizan la mayor información mutua, es decir la capacidad. La función devuelve la capacidad y el valor p que la otorga.

Para calcular la probabilidad de error, por cada salida (bj) se elige un a\* que otorga la mayor probabilidad, es decir, el menor error; luego se suma por cada columna la probabilidad de salida por la probabilidad de tener un error dada esa salida P(b) \* P(E/b); esto otorga la probabilidad de error, que se interpreta como la probabilidad de asumir una entrada incorrecta dada una salida, cuanto mayor el ruido mayor la probabilidad de error.



f) Para detectar errores en la secuencia de entrada, interpreto la entrada como un mensaje, siendo este una matriz de 4\*8 con 3 datos de 7 bits (ascii) con sus bits de paridad VRC, LRC y el de paridad cruzada. Luego verifico las filas y columnas que no cumplen la paridad par, si tengo más de 1 fila o columna que no cumplan la paridad, no se puede corregir el mensaje, recordar que β=1, se puede corregir hasta 1 error. Si la intersección de la fila y la columna que no cumple la paridad es el bit de paridad cruzada, entonces tampoco se puede corregir el mensaje. Si finalmente no se cumplen las condiciones anteriores invierto el bit que se encuentra en la intersección de la fila y la columna dada, así corrigiendo el mensaje.




* Análisis:



a) Las probabilidades se acercan a ser equiprobables, por lo que hay entropía cercana a 1.00.

Visualizando la matriz del canal se aprecia facilmente que hay 2 pares de columnas que son cl y por lo tanto se puede reducir la matriz a una binaria.


b) La matriz así como está no es ni determinante ni sin ruido, por lo que va a haber pérdida y ruido mayor a 0.



c) Lo anterior se comprueba con los valores H(A/B) = 0.7158; H(B/A) = 1.4686; I(A,B) = 0.2814. Con la ecuación I(A,B) = H(A) - H(A/B) se puede obtener la entropía de la entrada que es 0.9972, demonstrando lo dicho en el primer inciso. Luego la entropía de la salida, dado I(A,B) = H(B) - H(B/A), sería 1.75. De estos valores se pueden interpretar varias cosas:
La entropía de la salida es casi el doble que la de entrada, lo cual tiene sentido ya que hay 2 entradas y 4 salidas.
La entropía de la entrada tiende a 1, pero la información mutua es 0.2814, es decir se recupera muy poca información, esto debido al alto nivel de ruido

Hay mucha pérdida, es decir dada las entradas hay mucha incertidumbre sobre la salida.



d) Al efectuar las 2 reducciones posibles nos queda una matriz binaria 

&#x09;0.5294	0.4706
	1.0000	0.0000
Esta matriz, tiene menos pérdida, lógico por tener la mitad de columnas, y mantiene la información mutua de la matriz original, por ser reducción suficiente. Aquí incluso se puede apreciar más facilmente, que a pesar de que con una salida la entrada sea si o si un 1, con la otra salida hay mucha probabilidad tanto de una entrada como de otra.



e) La capacidad del canal es 0.2988, que es ligeramente más alta que la información mutua dadas las probabilidades a priori actuales.
Es decir que con las probabilidades actuales se acerca mucho a la máxima información mutua.

Y a la vez podemos concluir que el canal es extremadamente malo, ya que se pierde un 70% de la información que pasa desde la entrada, tiene mucho ruido.

La probabilidad de error es de .2812. Es decir que hay un 30% de probabilidades de interpretar un elemento de entradada erróneo desde la salida.



f) Dado que se encuentra una sola columna y fila con paridad incorrecta, y que su intersección no es el bit de paridad cruzada, es posible corregir el mensaje. Interpretando el mensaje como 3 caracteres ascii obtenenemos el mensaje "SOL", lo que hace entender que se decodificó el mensaje correctamente, ya que es un mensaje coherente.











