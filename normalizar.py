from dividir_polinomios import sumar_bits, obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio
from generar_campo_galois import generar_campo


def normalizar(pol:list[tuple[int,int]], tabla:list[list[int]]):
    alfa = pol[0][1]
    if alfa == 0:
        return 0
    else:
        alfa_normalizador = len(tabla)-1-alfa
        return alfa_normalizador

if __name__ == "__main__":
    campo = generar_campo([1,0,1,1], 8)
    print(normalizar([(1,5), (0,2)], campo))