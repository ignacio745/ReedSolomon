from generar_campo_galois import generar_campo
from dividir_polinomios import obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio, dividir_polinomios
from polinomio_generador import crear_polinomio_generador_palabras_validas
from polinomio_a_bytes import obtener_bytes_desde_polinomio
from math import lcm




def generar_palabra_valida(tamaño_byte: int, n: int, k: int, campo: list[list[int]], bytes_informacion_tamaño_correcto:list[list[int]]) -> list[list[int]]:
    # bits:list[int] = []

    # for byte in bytes_informacion:
    #     bits.extend([int(bit) for bit in f"{int(byte):08b}"])
    # print(bits)
    

    # bytes_informacion_tamaño_correcto = [bits[i:i+tamaño_byte] for i in range(0, len(bits), tamaño_byte)]
    # bytes_informacion_tamaño_correcto = bytes_informacion_tamaño_correcto[0:5]

    

    g_x = crear_polinomio_generador_palabras_validas(n, k, campo)
    polinomio_informacion = [(n-1-i, obtener_alfa_entero_desde_espacio(byte, campo)) for (i, byte) in enumerate(bytes_informacion_tamaño_correcto) if byte != campo[0]]

    resto = dividir_polinomios(campo, polinomio_informacion, g_x)[0]

    polinomio_completo = polinomio_informacion + resto

    bytes_completos = obtener_bytes_desde_polinomio(polinomio_completo, campo, n)
    return bytes_completos


def bytes_completos_a_archivo(lista_palabras_validas:list[list[list[int]]], tamaño_byte:int, nombre_archivo:str):
    cadena_bytes:str = ""
    for palabras_valida in lista_palabras_validas:
        for byte_completo in palabras_valida:
            cadena_bytes += "".join([str(bit) for bit in byte_completo])
    bytes_completos = [int(cadena_bytes[i:i+8], 2) for i in range(0, len(cadena_bytes), 8)]
    archivo = open(nombre_archivo, "wb")
    archivo.write(bytes(bytes_completos))
    archivo.close()


def generar_lista_palabras_validas(tamaño_bytes: int, n:int, k:int, campo:list[list[int]], bytes_informacion:bytes) -> list[list[list[int]]]:
    if len(bytes_informacion*8) % (tamaño_bytes * k) != 0:
        # bytes_informacion += bytes("\0" * ((tamaño_bytes * k - ((len(bytes_informacion)*8) % (tamaño_bytes * k))) // 8), "utf-8")
        cant_bits_informacion = len(bytes_informacion)*8
        bits_por_palabra = tamaño_bytes * k
        tamaño_minimo = lcm(8, bits_por_palabra)
        # print((tamaño_minimo*(cant_bits_informacion//tamaño_minimo+1) - cant_bits_informacion) // 8)
        bytes_informacion += bytes("\n" * ((tamaño_minimo*(cant_bits_informacion//tamaño_minimo+1) - cant_bits_informacion) // 8), "utf-8")
    # for i in bytes_informacion:
    #     print(i)
    # print(len(bytes_informacion))

    bits = "".join([f"{byte:08b}" for byte in bytes_informacion])
    bytes_informacion_correcto:list[list[int]] = [[int(bit) for bit in bits[i:i+tamaño_byte]] for i in range(0, len(bits), tamaño_byte)]
    # print(bytes_informacion_correcto)

    lista_palabras_validas = []
    for i in range(0, len(bytes_informacion_correcto), k):
        # print(bytes_informacion_correcto[i:i+k])
        nueva_valida = generar_palabra_valida(tamaño_bytes, n, k, campo, bytes_informacion_correcto[i:i+k])
        # print(nueva_valida)
        lista_palabras_validas.append(nueva_valida)
    return lista_palabras_validas





if __name__ == "__main__":

    # campo = generar_campo([1,0,1,1], 8)
    
    n = 15
    k = 9
    tamaño_byte = 4
    
    polinomio_campo:list[int] = [1,0,0,1,1]
    campo = generar_campo(polinomio_campo, 2**tamaño_byte)

    bytes_informacion_tamaño_correcto:list[list[int]] = []
    archivo = open("informacion.txt", "rb")
    bytes_informacion = archivo.read()
    archivo.close()



    palabras_validas = generar_lista_palabras_validas(tamaño_byte, n, k, campo, bytes_informacion)
    # for palabra_valida in palabras_validas:
    #     print(palabra_valida)

    # print(generar_palabra_valida(tamaño_byte, n, k, campo, b"ABCD"))
    
    bytes_completos_a_archivo(palabras_validas, tamaño_byte, "informacion_con_control_de_error.txt")