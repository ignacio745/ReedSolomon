from dividir_polinomios import obtener_alfa_desde_entero

def obtener_bytes_desde_polinomio(polinomio:list[tuple[int, int]], campo:list[list[int]], n: int):
    bytes:list[list[int]] = []
    cant = len(polinomio)


    bytes.extend([campo[0]]*(n-polinomio[0][0]-1))
    for i, comp in enumerate(polinomio):
        bytes.append(obtener_alfa_desde_entero(comp[1], campo))
        ceros = comp[0] - polinomio[i+1][0] - 1 if i+1 < cant else comp[0]
        bytes.extend([campo[0]]*ceros)
    return bytes