from dividir_polinomios import dividir_polinomios, sumar_polinomios, obtener_alfa_desde_entero, obtener_alfa_entero_desde_espacio, sumar_bits
from generar_campo_galois import generar_campo


def eliminar_repetidos(pol:list[tuple[int, int]], tabla:list[list[int]]):
    resultado: list[tuple[int, int]] = []
    grado = 0
    for comp in pol:
        grado = max(grado, comp[0])
    
    for grado_actual in range(grado, -1, -1):
        lista_actual:list[tuple[int, int]] = []
        for comp in pol:
            if comp[0] == grado_actual:
                lista_actual.append(comp)
        nuevo = [0,0,0,0]
        for comp in lista_actual:
            nuevo = sumar_bits(nuevo, obtener_alfa_desde_entero(comp[1], tabla))
        nuevo = obtener_alfa_entero_desde_espacio(nuevo, tabla)
        if nuevo != -1:
            resultado.append((grado_actual, nuevo))
    return resultado



def multiplicar_polinomios(pol_1:list[tuple[int, int]], pol_2:list[tuple[int, int]], tabla:list[list[int]]):
    aux:list[tuple[int,int]] = []
    for comp_1 in pol_1:
        for comp_2 in pol_2:
            alfa_nuevo = comp_1[1]+comp_2[1]
            alfa_nuevo = obtener_alfa_entero_desde_espacio(obtener_alfa_desde_entero(alfa_nuevo, tabla), tabla)
            aux.append((comp_1[0]+comp_2[0], alfa_nuevo))
    
    pol_nuevo = eliminar_repetidos(aux, tabla)
    return pol_nuevo



def obtener_normalizador(polinomio:list[tuple[int, int]], campo:list[list[int]]):
    if polinomio[0][1] == 0:
        return [(0,0)]
    normalizador = [(0, len(campo) - 1 - polinomio[0][1])]
    return normalizador






def euclides(pol_1:list[tuple[int, int]], pol_2:list[tuple[int, int]], n:int , k:int, campo: list[list[int]]):
    penult = pol_1.copy()
    ult = pol_2.copy()
    actual, q = dividir_polinomios(campo, penult, ult)
    t_actual = q
    t_anterior = ([(0,0)])
    while len(actual) > 0 and actual[0][0] > ((n-k)//2)-1:
        penult = ult.copy()
        ult = actual.copy()
        actual, q = dividir_polinomios(campo, penult, ult)
        t_por_q = multiplicar_polinomios(t_actual, q, campo)
        aux = sumar_polinomios(t_anterior, t_por_q, campo)
        t_anterior = t_actual
        t_actual = aux
    
    normalizador = obtener_normalizador(t_actual, campo)
    t_normalizado = multiplicar_polinomios(t_actual, normalizador, campo)
    gamma_normalizado = multiplicar_polinomios(actual, normalizador, campo)
    return t_normalizado, gamma_normalizado



if __name__ == "__main__":
    campo = generar_campo([1,0,0,1,1], 16)
    print(euclides([(4,0)], [(3,11), (2, 11), (1, 4), (0, 12)], 15, 11, campo))
    campo = generar_campo([1,0,1,1], 8)
    print(euclides([(2,0)], [(1,2), (0, 6)], 7, 5, campo))