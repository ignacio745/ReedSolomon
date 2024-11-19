from dividir_polinomios import sumar_bits, obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio

def sumar_con_alfa(polinomio:list[tuple[int, int]], alfa:int, campo: list[list[int]]):
    nuevo:list[int] = []

    for comp in polinomio:
        nuevo.append(comp[0]*alfa+comp[1])
    resultado = obtener_alfa_desde_entero(-1, campo)
    for comp in nuevo:
        resultado = sumar_bits(resultado, obtener_alfa_desde_entero(comp, campo))
    resultado = obtener_alfa_entero_desde_espacio(resultado, campo)
    return resultado


def obtener_sindrome(polinomio:list[tuple[int, int]], campo: list[list[int]], capacidad_correccion:int):
    sindrome:list[tuple[int,int]] = []
    n_k = capacidad_correccion * 2
    for i in range(1, n_k+1):
        alfa = sumar_con_alfa(polinomio, i, campo)
        if alfa != -1:
            # sindrome.append(i-1, alfa)
            sindrome = [(i-1, alfa)] + sindrome
    return sindrome