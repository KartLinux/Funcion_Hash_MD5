#Leer un archivo con el texto a cifrar
#Generar y/o imprimir la(las) claves de cifrado
#Cifrar e imprimir el texto cifrado.
#Descifrar e imprimir el texto claro.
#Luego de cada etapa, muestre tiempo transcurrido.
#Repita el proceso con archivos de diferente número de palabras (10, 100, 1000, 10000, 100000 y 1000000). 

#Genere una tabla resumen con todos los resultados. 
#Esta tabla debe tener como filas, el nombre de cada uno de los algoritmos 
#implementados y las siguientes columnas: #palabras, T-E1, T-E2, T-E3, T-E4, T-Total.

#-------------------------------------------------------------------------------------
import math
import struct
import time
# 1 primer paso RRELLENO
def md5_padding(message):
    # Calcular la longitud del mensaje en bits
    message_length = len(message) * 8

    # Agregar un bit "1" seguido de ceros
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"

    # Agregar la longitud del mensaje como un entero sin signo de 64 bits
    # byteorder little siginifica el orden de bytes con formato little-endian
    # el argumento 8 significa que debe utilizar 8 bytes para representar el numero
    message += message_length.to_bytes(8, byteorder="little")

    return message


    # 2 segundo paso INICIALIZACION
    #toma un mensaje como parámetro y devuelve una lista de bloques de 512 bits. 
    # La función divide el mensaje en bloques de 64 bytes (512 bits) y los agrega a una lista.
def md5_split_blocks(message):
    # Dividir el mensaje en bloques de 512 bits (64 bytes)
    blocks = []
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        # para tranformar en un formato de numeros enteros y meterlos en el paso de procesamiento
        # formato little-endian
        values = list(struct.unpack('<' + 'I'*16, block))#cada lista de 16 numeros
        blocks.append(values)
    return blocks

    # tercer paso procesamiento
# valores en hexadecimales (0x), base 16, A ala F son valores de 100 al 15
a0 = 0x67452301
b0 = 0xefcdab89
c0 = 0x98badcfe
d0 = 0x10325476

def md5_process(block, a0, b0, c0, d0):
    # Constantes para cada 
    #variable S contiene las constantes de desplazamiento utilizadas en cada ronda del procesamiento 
    # y siempre deben ser los mismos valores definidos en el estándar MD5.
    S = [[7, 12, 17, 22]] * 4 + [[5, 9, 14, 20]] * 4 + [[4, 11, 16, 23]] * 4 + [[6, 10, 15, 21]] * 4
    #& 0xFFFFFFFF se utiliza para asegurar que el resultado de la operación sea un número de 32 bits.
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    
    # Inicialización de variables
    A, B, C, D = a0, b0, c0, d0
    
    # Procesamiento de bloques
    # ^ operador XOR a nivel de bits
    # ~ es el operador NOT a nivel de bits
    # | es el operador OR a nivel de bits
    # & es el operador AND a nivel de bits
    for i in range(64):
        if i < 16:
            F = (B & C) | ((~B) & D)
            g = i
        elif i < 32:
            F = (D & B) | ((~D) & C)
            g = (5*i + 1) % 16
        elif i < 48:
            F = B ^ C ^ D
            g = (3*i + 5) % 16
        else:
            F = C ^ (B | (~D))
            g = (7*i) % 16
        
        dTemp = D
        D = C
        C = B
        B = B + left_rotate((A + F + K[i] + block[g]) & 0xffffffff, S[i//16][i%4])
        A = dTemp
    
    # Suma de resultados al hash anterior
    a0 = (a0 + A) & 0xFFFFFFFF
    b0 = (b0 + B) & 0xFFFFFFFF
    c0 = (c0 + C) & 0xFFFFFFFF
    d0 = (d0 + D) & 0xFFFFFFFF
    
    return a0, b0, c0, d0

def left_rotate(x, c):
    # << para desplazar los bits de (x) hacia la izquierda(c) posiciones
    return (x << c) | (x >> (32 - c))
#==============================================================================================================
#message = b"Hello, world!, que hay mijin flow, esteo es un texto muuy largo de prueba quiero ver hasta donde esta capas y que va hacer la funcion"

start_time_read = time.time()
with open('D:\Documentos\Pruebas en VSual Code\Python\Archivos txt\\archivo10.txt', 'rb') as f:
    message = f.read()
end_time_read =time.time()
#------------------------------------- Empieza funcion para el hash
#========================
#   Inicio de tiempo    |
#========================
start_time = time.time()
padded_message = md5_padding(message)
#
#print(padded_message)
blocks = md5_split_blocks(padded_message)
#print(blocks)
for block in blocks:
    a0, b0, c0, d0 = md5_process(block, a0, b0, c0, d0)
# 4 cuarto paso 
# salida, donde se concatenan las variables a0, b0, c0 y d0 en el orden inverso para formar el hash final
result = d0.to_bytes(4, byteorder="little") + c0.to_bytes(4, byteorder="little") + b0.to_bytes(4, byteorder="little") + a0.to_bytes(4, byteorder="little")
#print(result)
result_hex = result.hex()
print(result_hex)
#-------------------------------------Termina la funcion del hash
end_time =time.time()

#Calculamos el tiempo en milesegundos
duration = (end_time_read - start_time_read) * 1000
print(f"La lectura tardó {duration:.2f} milisegundos en ejecutarse")
duration = (end_time - start_time) * 1000
print(f"La función tardó {duration:.2f} milisegundos en ejecutarse")
#----
