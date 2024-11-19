from sindrome import obtener_sindrome
from bytes_a_polinomio import obtener_polinomio_desde_bytes
from generar_campo_galois import generar_campo
from dividir_polinomios import obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio, dividir_polinomios, sumar_bits
from euclides import euclides
from raiz import obtener_raices, obtener_resultado
from derivada import derivar
from polinomio_generador import crear_polinomio_generador_palabras_validas


def recuperar_bytes(palabra:list[list[int]], n:int, k:int, campo:list[list[int]]):
    polinomio = obtener_polinomio_desde_bytes(palabra, campo)


    capacidad_correccion = (n-k)//2
    sindrome = obtener_sindrome(polinomio, campo, capacidad_correccion)
    if len(sindrome) == 0:
        return [i.copy() for i in palabra]
    
    t_normalizado, gamma_normalizado = euclides([(n-k, 0)], sindrome, n, k, campo)

    raices = obtener_raices(t_normalizado, campo)


    potencias_con_error = [(len(campo) - 1 - i)%(len(campo)-1) for i in raices]


    t_norm_derivado = derivar(t_normalizado)
    
    errores:list[int] = []
    for raiz in raices:
        gamma_evaluado = obtener_resultado(gamma_normalizado, campo, raiz)
        t_norm_deriv_evaluado = obtener_resultado(t_norm_derivado, campo, raiz)
        errores.append((gamma_evaluado-t_norm_deriv_evaluado) % (len(campo)-1))
    
    
    arreglado = [componente.copy() for componente in palabra]
    for potencia, error in zip(potencias_con_error, errores):
        patron_error = obtener_alfa_desde_entero(error, campo)
        arreglado[-potencia-1] = sumar_bits(arreglado[-potencia-1], patron_error)
    
    return arreglado





def desarmar_entrelazado(bits:str, n:int, tamaño_byte:int, cant_entrelazados:int) -> str:
    cant_bits_entrelazados = tamaño_byte * n * cant_entrelazados
    bits_desentrelazados = ""
    bits_por_palabra = tamaño_byte * n
    for i in range(0, len(bits), cant_bits_entrelazados):
        bits_actuales = bits[i:i+cant_bits_entrelazados]
        for j in range(cant_entrelazados):
            for k in range(bits_por_palabra):
                bits_desentrelazados += bits_actuales[k * cant_entrelazados + j]
    return bits_desentrelazados


    




if __name__ == "__main__":
    # n = 7
    # k = 5
    # tamaño_byte = 3
    # polinomio_campo = [1, 0, 1, 1]
    # campo = generar_campo(polinomio_campo, 2**tamaño_byte)

    # palabra = [[0,1,0], [0,0,0], [0,1,0], [1,1,1], [0,0,1], [0,0,0], [1,0,1]]

    # recuperado = recuperar_bytes(palabra, n, k, campo)
    # print(recuperado)


    # n = 15
    # k = 11
    # tamaño_byte = 4
    # polinomio_campo = [1,0,0,1,1]
    # campo = generar_campo(polinomio_campo, 2**tamaño_byte)

    # # bytes = [[0,1,0,1], [0,0,1,0], [0,1,0,0], [0,0,0,1], [0,1,0,0], [0,0,1,1], [0,1,0,0], [1,0,0,1], [0,1,0,0], [1,1,1,0], [0,1,0,0], [0,1,0,0], [0,0,1,1], [1,0,0,1]]

    # palabra = [obtener_alfa_desde_entero(alfa, campo) for alfa in [8,1,2,0,2,4,2,12,2,11,2,2,4,1,14]]

    # recuperado = recuperar_bytes(palabra, n, k, campo)
    # print(recuperado)
    # recuperado_enteros = [alfa_entero for alfa_entero in map(lambda x: obtener_alfa_entero_desde_espacio(x, campo), recuperado)]
    # print(recuperado_enteros)

    n = 15
    k= 9
    tamaño_byte = 4
    polinomio_campo = [1,0,0,1,1]
    campo = generar_campo(polinomio_campo, 2**tamaño_byte)

    archivo = open("informacion_corrompida.txt", "rb")
    bytes_iniciales = archivo.read()
    archivo.close()

    bits = "".join([f"{byte:08b}" for byte in bytes_iniciales])

    bits_desentrelazados = desarmar_entrelazado(bits, n, tamaño_byte, 10)
    
    bytes_tamaño_correcto:list[list[int]] = [[int(bit) for bit in bits_desentrelazados[i:i+tamaño_byte]] for i in range(0, len(bits_desentrelazados), tamaño_byte)]
    
    palabras:list[list[list[int]]] = [bytes_tamaño_correcto[i:i+n] for i in range(0, len(bytes_tamaño_correcto), n)]


    recuperado_informacion:list[list[int]] = []
    for palabra in palabras:

        recuperado = recuperar_bytes(palabra, n, k, campo)
        recuperado_informacion.extend(recuperado[:k])

        recuperado_enteros = [alfa_entero for alfa_entero in map(lambda x: obtener_alfa_entero_desde_espacio(x, campo), recuperado)]


    
    bits_informacion:str = "".join("".join([str(bit) for bit in byte]) for byte in recuperado_informacion)

    bytes_informacion = bytes([int(bits_informacion[i:i+8], 2) for i in range(0, len(bits_informacion), 8)])

    archivo = open("informacion_recuperada.txt", "wb")
    archivo.write(bytes_informacion)
    archivo.close()