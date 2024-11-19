from dividir_polinomios import obtener_alfa_entero_desde_espacio

def obtener_polinomio_desde_bytes(bytes:list[list[int]], campo:list[list[int]]):
    polinomio:list[tuple[int,int]] = []
    for i, byte in enumerate(bytes):
        if byte != campo[0]:
            polinomio.append((len(bytes)-1-i, obtener_alfa_entero_desde_espacio(byte, campo)))
    return polinomio