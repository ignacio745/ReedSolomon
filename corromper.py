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


    bytes_corrompidos = bytes([int(bits_corrompidos[i:i+8], 2) for i in range(0, len(bits_corrompidos), 8)])

    archivo = open("informacion_corrompida.txt", "wb")
    archivo.write(bytes_corrompidos)
    archivo.close()