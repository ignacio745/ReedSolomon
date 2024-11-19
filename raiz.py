from dividir_polinomios import obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio, sumar_bits
from generar_campo_galois import generar_campo


def obtener_resultado(pol:list[tuple[int,int]], tabla:list[list[int]], alfa_entero:int):
    resultado = [0 for _ in range(len(tabla[0]))]
    for comp in pol:
        if alfa_entero == -1 and comp[0] != 0:
            total = -1
        else:
            primer_componente = alfa_entero * comp[0]
            segunda_componente = comp[1]
            total = primer_componente + segunda_componente
        resultado = sumar_bits(resultado, obtener_alfa_desde_entero(total, tabla))
    resultado = obtener_alfa_entero_desde_espacio(resultado, tabla)
    return resultado





def obtener_raices(pol:list[tuple[int,int]], tabla:list[list[int]]):
    raices:list[int] = []
    for alfa_entero in range(0, len(tabla)-1):
        if obtener_resultado(pol, tabla, alfa_entero) == -1:
            raices.append(alfa_entero)
    return raices

if __name__ == "__main__":
    print(obtener_raices([(1,0), (0,4)], generar_campo([1,0,1,1], 8)))
    print(obtener_raices([(2,0), (1,8)], generar_campo([1,0,0,1,1], 16)))