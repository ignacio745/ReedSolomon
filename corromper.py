import random


def crear_lista_posiciones_errores(n:int, errores_soportables:int) -> list:
    """
    Crea una lista de posiciones de errores a partir de un número n y una cantidad de errores soportables.
    """
    lista_posiciones_errores = []
    for i in range(errores_soportables):
        posicion = random.randint(0, n-1)
        while posicion in lista_posiciones_errores:
            posicion = random.randint(0, n-1)
        lista_posiciones_errores.append(posicion)
    return lista_posiciones_errores

if __name__ == "__main__":
    archivo = open("informacion_con_control_de_error.txt", "rb")
    bytes_iniciales = archivo.read()
    archivo.close()

    bits = "".join([f"{byte:08b}" for byte in bytes_iniciales])
    

    tamaño_byte = 4
    n = 15
    k = 9
    cant_entrelazados = 10

    errores_soportables = (n-k)*cant_entrelazados//2

    bits_corrompidos = ""
    for i in range(errores_soportables):
        bits_corrompidos += str(random.randint(0, 1))
    bits_corrompidos += bits[errores_soportables:]


    
    # errores_soportables = (n-k)//2

    # lista_bits = [int(bit) for bit in bits]
    

    # for i in range(0, len(lista_bits), n*tamaño_byte):
    #     palabra = lista_bits[i:i+n*tamaño_byte]
    #     posiciones_errores = crear_lista_posiciones_errores(n, errores_soportables)

    #     for posicion in posiciones_errores:
    #         palabra[posicion*tamaño_byte:posicion*tamaño_byte+tamaño_byte] = [random.randint(0, 1) for _ in range(tamaño_byte)]
        
    #     lista_bits[i:i+n*tamaño_byte] = palabra

    # bits_corrompidos = "".join([str(bit) for bit in lista_bits])

    bytes_corrompidos = bytes([int(bits_corrompidos[i:i+8], 2) for i in range(0, len(bits_corrompidos), 8)])

    archivo = open("informacion_corrompida.txt", "wb")
    archivo.write(bytes_corrompidos)
    archivo.close()