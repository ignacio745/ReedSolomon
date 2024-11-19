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


def bytes_completos_a_archivo(lista_palabras_validas:list[list[list[int]]], n:int, tamaño_byte:int, nombre_archivo:str, cant_entrelazados:int) -> None:
    cadena_bytes:str = ""
    for palabras_valida in lista_palabras_validas:
        for byte_completo in palabras_valida:
            cadena_bytes += "".join([str(bit) for bit in byte_completo])
    # bytes_completos = [int(cadena_bytes[i:i+8], 2) for i in range(0, len(cadena_bytes), 8)]
    
    bits_entrelazados:str = ""
    bits_por_palabra = tamaño_byte * n
    for k in range(0, len(cadena_bytes), bits_por_palabra*cant_entrelazados):
        bits_actuales = cadena_bytes[k:k+bits_por_palabra*cant_entrelazados]
        for i in range(bits_por_palabra):
            for j in range(cant_entrelazados):
                bits_entrelazados += bits_actuales[bits_por_palabra * j + i]

    



    bytes_completos:list[int] = [int(bits_entrelazados[i:i+8], 2) for i in range(0, len(bits_entrelazados), 8)]
    archivo = open(nombre_archivo, "wb")
    archivo.write(bytes(bytes_completos))
    archivo.close()


def generar_lista_palabras_validas(tamaño_bytes: int, n:int, k:int, campo:list[list[int]], bytes_informacion:bytes, cant_entrelazados:int) -> list[list[list[int]]]:
    bits_por_palabra_informacion = tamaño_bytes * k
    if len(bytes_informacion*8) % (bits_por_palabra_informacion) != 0:
        cant_bits_informacion = len(bytes_informacion)*8
        tamaño_minimo = lcm(8, bits_por_palabra_informacion)

        bytes_informacion += bytes("\n" * ((tamaño_minimo*(cant_bits_informacion//tamaño_minimo+1) - cant_bits_informacion) // 8), "utf-8")

        cant_bits_producidos = len(bytes_informacion) * 8 // k * n

        bits_por_entrelazado = tamaño_bytes * n * cant_entrelazados

        bits_producidos_faltantes = bits_por_entrelazado - (cant_bits_producidos % bits_por_entrelazado)
        
        cant_bits_faltantes = bits_producidos_faltantes * k // n

        bytes_informacion += bytes("\n" * (cant_bits_faltantes // 8), "utf-8")




    bits = "".join([f"{byte:08b}" for byte in bytes_informacion])
    bytes_informacion_correcto:list[list[int]] = [[int(bit) for bit in bits[i:i+tamaño_bytes]] for i in range(0, len(bits), tamaño_bytes)]


    lista_palabras_validas:list[list[list[int]]] = []
    for i in range(0, len(bytes_informacion_correcto), k):
        nueva_valida = generar_palabra_valida(tamaño_bytes, n, k, campo, bytes_informacion_correcto[i:i+k])
        lista_palabras_validas.append(nueva_valida)
    

    


    return lista_palabras_validas





if __name__ == "__main__":

    # campo = generar_campo([1,0,1,1], 8)
    
    n = 15
    k = 9
    tamaño_byte = 4
    
    polinomio_campo:list[int] = [1,0,0,1,1]
    campo = generar_campo(polinomio_campo, 2**tamaño_byte)
    cant_entrelazados = 10

    bytes_informacion_tamaño_correcto:list[list[int]] = []
    archivo = open("informacion.txt", "rb")
    bytes_informacion = archivo.read()
    archivo.close()



    palabras_validas = generar_lista_palabras_validas(tamaño_byte, n, k, campo, bytes_informacion, cant_entrelazados)
    # for palabra_valida in palabras_validas:
    #     print(palabra_valida)

    # print(generar_palabra_valida(tamaño_byte, n, k, campo, b"ABCD"))
    
    bytes_completos_a_archivo(palabras_validas, n, tamaño_byte, "informacion_con_control_de_error.txt", cant_entrelazados)